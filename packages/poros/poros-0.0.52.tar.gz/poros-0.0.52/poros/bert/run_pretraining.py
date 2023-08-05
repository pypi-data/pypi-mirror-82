# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Run masked LM/next sentence masked_lm pre-training for BERT."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from poros.bert import modeling
from poros.bert import optimization
import tensorflow as tf
from absl import flags
from absl import app
import logging
from poros.poros_train import restore
import tensorflow_addons as tfa


FLAGS = flags.FLAGS

## Required parameters
flags.DEFINE_string(
    "bert_config_file", None,
    "The config json file corresponding to the pre-trained BERT model. "
    "This specifies the model architecture.")

flags.DEFINE_string(
    "input_file", None,
    "Input TF example files (can be a glob or comma separated).")

flags.DEFINE_string(
    "output_dir", None,
    "The output directory where the model checkpoints will be written.")

## Other parameters
flags.DEFINE_string(
    "init_checkpoint", None,
    "Initial checkpoint (usually from a pre-trained BERT model).")

flags.DEFINE_integer(
    "max_seq_length", 128,
    "The maximum total input sequence length after WordPiece tokenization. "
    "Sequences longer than this will be truncated, and sequences shorter "
    "than this will be padded. Must match data generation.")

flags.DEFINE_integer(
    "max_predictions_per_seq", 20,
    "Maximum number of masked LM predictions per sequence. "
    "Must match data generation.")

flags.DEFINE_bool("do_train", False, "Whether to run training.")

flags.DEFINE_bool("do_eval", False, "Whether to run eval on the dev set.")

flags.DEFINE_integer("train_batch_size", 32, "Total batch size for training.")

flags.DEFINE_integer("eval_batch_size", 8, "Total batch size for eval.")

flags.DEFINE_float("learning_rate", 5e-5, "The initial learning rate for Adam.")

flags.DEFINE_integer("num_train_steps", 100000, "Number of training steps.")

flags.DEFINE_integer("num_warmup_steps", 10000, "Number of warmup steps.")

flags.DEFINE_integer("save_checkpoints_steps", 1000,
                     "How often to save the model checkpoint.")

flags.DEFINE_integer("iterations_per_loop", 1000,
                     "How many steps to make in each estimator call.")

flags.DEFINE_integer("max_eval_steps", 100, "Maximum number of eval steps.")

flags.DEFINE_bool("use_tpu", False, "Whether to use TPU or GPU/CPU.")

flags.DEFINE_string(
    "tpu_name", None,
    "The Cloud TPU to use for training. This should be either the name "
    "used when creating the Cloud TPU, or a grpc://ip.address.of.tpu:8470 "
    "url.")

flags.DEFINE_string(
    "tpu_zone", None,
    "[Optional] GCE zone where the Cloud TPU is located in. If not "
    "specified, we will attempt to automatically detect the GCE project from "
    "metadata.")

flags.DEFINE_string(
    "gcp_project", None,
    "[Optional] Project name for the Cloud TPU-enabled project. If not "
    "specified, we will attempt to automatically detect the GCE project from "
    "metadata.")

flags.DEFINE_string("master", None, "[Optional] TensorFlow master URL.")

flags.DEFINE_integer(
    "num_tpu_cores", 8,
    "Only used if `use_tpu` is True. Total number of TPU cores to use.")


class SiameseBertModel(tf.keras.Model):

    def __init__(self, config, is_training, init_checkpoint=None, use_one_hot_embeddings=False, **kwargs):
        super(SiameseBertModel, self).__init__()
        self.bert_config = config
        self.bert_layer = modeling.BertLayer(config=config, is_training=is_training)
        self.use_one_hot_embeddings = use_one_hot_embeddings
        self.use_tpu = False
        self.init_checkpoint = init_checkpoint
        self.init_from_checkpoint()
        self.loss_layer = tfa.losses.ContrastiveLoss()

    def init_from_checkpoint(self):
        if not self.init_checkpoint:
            return
        tvars = self.trainable_variables
        restore.init_from_checkpoint(self.init_checkpoint, tvars)

    def call(self, features):
        input_ids_a = features["input_ids_a"]
        input_mask_a = features["input_mask_a"]
        input_ids_b = features["input_ids_b"]
        input_mask_b = features["input_mask_b"]
        y_true = tf.reshape(features["label_id"], shape=[-1])

        bert_layer_output_1 = self.bert_layer(
            input_ids_a,
            input_mask_a,
            None,
            "bert",
            self.use_one_hot_embeddings
        )
        bert_layer_output_2 = self.bert_layer(
            input_ids_b,
            input_mask_b,
            None,
            "bert",
            self.use_one_hot_embeddings
        )

        y_pred = tf.linalg.norm(bert_layer_output_2 - bert_layer_output_1, axis=-1)
        loss = self.loss_layer(y_true=y_true, y_pred=y_pred)

        self.add_loss(loss)
        return y_pred


class BertPretrainModel(tf.keras.Model):

    def __init__(self, config, is_training, init_checkpoint=None, use_one_hot_embeddings=False, **kwargs):
        super(BertPretrainModel, self).__init__()
        self.bert_config = config
        self.bert_layer = modeling.BertLayer(config=config, is_training=is_training)
        self.use_one_hot_embeddings = use_one_hot_embeddings
        self.use_tpu = False
        self.init_checkpoint = init_checkpoint
        self.mask_lm_layer = MaskLmLayer(bert_config=config)
        self.next_sentence_layer = NextSentenceLayer(bert_config=config)
        self.masked_lm_accuracy = None
        self.masked_lm_mean_loss = None
        self.init_from_checkpoint()
        self.masked_lm_mean_loss_metric = tf.metrics.Mean(name="masked_lm_mean_loss")
        self.masked_lm_accuracy_metric = tf.metrics.Accuracy(name="masked_lm_accuracy")
        self.next_sentence_accuracy_metric = tf.metrics.Accuracy(name="next_sentence_accuracy")
        self.next_sentence_mean_loss_metric = tf.metrics.Mean(name="next_sentence_mean_loss")

    def init_from_checkpoint(self):
        if not self.init_checkpoint:
            return
        tvars = self.trainable_variables
        restore.init_from_checkpoint(self.init_checkpoint, tvars)
        self.predict

    def call(self, features, training=False):
        input_ids = features["input_ids"]
        input_mask = features["input_mask"]
        segment_ids = features["segment_ids"]
        masked_lm_positions = features["masked_lm_positions"]
        masked_lm_ids = features["masked_lm_ids"]
        masked_lm_weights = features["masked_lm_weights"]
        next_sentence_labels = features["next_sentence_labels"]
        bert_layer_output = self.bert_layer(
            input_ids,
            input_mask,
            segment_ids,
            "bert",
            self.use_one_hot_embeddings,
            training=training
        )
        masked_lm_input = self.bert_layer.get_sequence_output()
        masked_lm_loss, masked_lm_example_loss, masked_lm_log_probs = \
            self.mask_lm_layer(masked_lm_input,
                               self.bert_layer.get_embedding_table(),
                               masked_lm_positions,
                               masked_lm_ids,
                               masked_lm_weights)

        (next_sentence_loss, next_sentence_example_loss, next_sentence_log_probs) = \
            self.next_sentence_layer(bert_layer_output, next_sentence_labels)
        total_loss = masked_lm_loss + next_sentence_loss
        self.add_loss(total_loss)
        next_sentence_log_probs = tf.reshape(
            next_sentence_log_probs, [-1, next_sentence_log_probs.shape[-1]])
        next_sentence_predictions = tf.argmax(
            next_sentence_log_probs, axis=-1, output_type=tf.int32)

        masked_lm_log_probs = tf.reshape(masked_lm_log_probs,
                                         [-1, masked_lm_log_probs.shape[-1]])
        masked_lm_predictions = tf.argmax(
            masked_lm_log_probs, axis=-1, output_type=tf.int32)
        masked_lm_ids = tf.reshape(masked_lm_ids, [-1])
        masked_lm_weights = tf.reshape(masked_lm_weights, [-1])
        masked_lm_accuracy_metric = self.masked_lm_accuracy_metric(y_pred=masked_lm_predictions, y_true=masked_lm_ids, sample_weight=masked_lm_weights)
        masked_lm_mean_loss_metric = self.masked_lm_mean_loss_metric(masked_lm_example_loss, sample_weight=masked_lm_weights)
        next_sentence_accuracy_metric = self.next_sentence_accuracy_metric(y_pred=next_sentence_predictions, y_true=next_sentence_labels)
        next_sentence_loss_metric = self.next_sentence_mean_loss_metric(next_sentence_loss)

        if not self.built:
            self.add_metric(masked_lm_accuracy_metric, aggregation='mean', name="masked_lm_accuracy")
            self.add_metric(masked_lm_mean_loss_metric, name="masked_lm_mean_loss")
            self.add_metric(next_sentence_accuracy_metric, aggregation='mean', name="next_sentence_accuracy")
            self.add_metric(next_sentence_loss_metric, name="next_sentence_mean_loss")
        self.summary()
        return bert_layer_output, total_loss


def model_fn_builder(bert_config, init_checkpoint, learning_rate,
                     num_train_steps, num_warmup_steps, use_tpu,
                     use_one_hot_embeddings):
    """Returns `model_fn` closure for TPUEstimator."""

    def model_fn(features, labels, mode, params):  # pylint: disable=unused-argument
        """The `model_fn` for TPUEstimator."""

        tf.get_logger().info("*** Features ***")
        for name in sorted(features.keys()):
            tf.get_logger().info("  name = %s, shape = %s" % (name, features[name].shape))

        input_ids = features["input_ids"]
        input_mask = features["input_mask"]
        segment_ids = features["segment_ids"]
        masked_lm_positions = features["masked_lm_positions"]
        masked_lm_ids = features["masked_lm_ids"]
        masked_lm_weights = features["masked_lm_weights"]
        next_sentence_labels = features["next_sentence_labels"]

        is_training = (mode == tf.estimator.ModeKeys.TRAIN)

        model = modeling.BertModel(
            config=bert_config,
            is_training=is_training,
            input_ids=input_ids,
            input_mask=input_mask,
            token_type_ids=segment_ids,
            use_one_hot_embeddings=use_one_hot_embeddings)

        (masked_lm_loss,
         masked_lm_example_loss, masked_lm_log_probs) = get_masked_lm_output(
            bert_config, model.get_sequence_output(), model.get_embedding_table(),
            masked_lm_positions, masked_lm_ids, masked_lm_weights)

        (next_sentence_loss, next_sentence_example_loss,
         next_sentence_log_probs) = get_next_sentence_output(
            bert_config, model.get_pooled_output(), next_sentence_labels)

        total_loss = masked_lm_loss + next_sentence_loss

        tvars = tf.compat.v1.trainable_variables()

        initialized_variable_names = {}
        scaffold_fn = None
        if init_checkpoint:
            (assignment_map, initialized_variable_names
             ) = modeling.get_assignment_map_from_checkpoint(tvars, init_checkpoint)
            if use_tpu:

                def tpu_scaffold():
                    tf.compat.v1.train.init_from_checkpoint(init_checkpoint, assignment_map)
                    return tf.compat.v1.train.Scaffold()

                scaffold_fn = tpu_scaffold
            else:
                tf.compat.v1.train.init_from_checkpoint(init_checkpoint, assignment_map)

        tf.get_logger().info("**** Trainable Variables ****")
        for var in tvars:
            init_string = ""
            if var.name in initialized_variable_names:
                init_string = ", *INIT_FROM_CKPT*"
            tf.get_logger().info("  name = %s, shape = %s%s", var.name, var.shape,
                            init_string)

        output_spec = None
        if mode == tf.estimator.ModeKeys.TRAIN:
            train_op = optimization.create_optimizer(
                total_loss, learning_rate, num_train_steps, num_warmup_steps, use_tpu)

            output_spec = tf.contrib.tpu.TPUEstimatorSpec(
                mode=mode,
                loss=total_loss,
                train_op=train_op,
                scaffold_fn=scaffold_fn)
        elif mode == tf.estimator.ModeKeys.EVAL:

            def metric_fn(masked_lm_example_loss, masked_lm_log_probs, masked_lm_ids,
                          masked_lm_weights, next_sentence_example_loss,
                          next_sentence_log_probs, next_sentence_labels):
                """Computes the loss and accuracy of the model."""
                masked_lm_log_probs = tf.reshape(masked_lm_log_probs,
                                                 [-1, masked_lm_log_probs.shape[-1]])
                masked_lm_predictions = tf.argmax(
                    masked_lm_log_probs, axis=-1, output_type=tf.int32)
                masked_lm_example_loss = tf.reshape(masked_lm_example_loss, [-1])
                masked_lm_ids = tf.reshape(masked_lm_ids, [-1])
                masked_lm_weights = tf.reshape(masked_lm_weights, [-1])
                masked_lm_accuracy = tf.metrics.accuracy(
                    labels=masked_lm_ids,
                    predictions=masked_lm_predictions,
                    weights=masked_lm_weights)
                masked_lm_mean_loss = tf.metrics.mean(
                    values=masked_lm_example_loss, weights=masked_lm_weights)

                next_sentence_log_probs = tf.reshape(
                    next_sentence_log_probs, [-1, next_sentence_log_probs.shape[-1]])
                next_sentence_predictions = tf.argmax(
                    next_sentence_log_probs, axis=-1, output_type=tf.int32)
                next_sentence_labels = tf.reshape(next_sentence_labels, [-1])
                next_sentence_accuracy = tf.metrics.accuracy(
                    labels=next_sentence_labels, predictions=next_sentence_predictions)
                next_sentence_mean_loss = tf.metrics.mean(
                    values=next_sentence_example_loss)

                return {
                    "masked_lm_accuracy": masked_lm_accuracy,
                    "masked_lm_loss": masked_lm_mean_loss,
                    "next_sentence_accuracy": next_sentence_accuracy,
                    "next_sentence_loss": next_sentence_mean_loss,
                }

            eval_metrics = (metric_fn, [
                masked_lm_example_loss, masked_lm_log_probs, masked_lm_ids,
                masked_lm_weights, next_sentence_example_loss,
                next_sentence_log_probs, next_sentence_labels
            ])
            output_spec = tf.contrib.tpu.TPUEstimatorSpec(
                mode=mode,
                loss=total_loss,
                eval_metrics=eval_metrics,
                scaffold_fn=scaffold_fn)
        else:
            raise ValueError("Only TRAIN and EVAL modes are supported: %s" % (mode))

        return output_spec

    return model_fn


class MaskLmLayer(tf.keras.layers.Layer):

    def __init__(self, bert_config):
        super(MaskLmLayer, self).__init__()
        self.bert_config = bert_config
        with tf.name_scope("cls/predictions"):
            # We apply one more non-linear transformation before the output layer.
            # This matrix is not used after pre-training.
            with tf.name_scope("transform"):
                with tf.name_scope("dense"):
                    self.layer_dense = tf.keras.layers.Dense(
                        units=self.bert_config.hidden_size,
                        activation=modeling.get_activation(self.bert_config.hidden_act),
                        kernel_initializer=modeling.create_initializer(self.bert_config.initializer_range)
                    )
                    self.layer_dense.build(input_shape=[None, self.bert_config.hidden_size])

                with tf.name_scope("LayerNorm"):
                    self.layer_norm = tf.keras.layers.LayerNormalization(epsilon=0.00001)
                    self.layer_norm.build(input_shape=[None, self.bert_config.hidden_size])

            self.output_bias = tf.Variable(
                name="output_bias",
                initial_value=tf.zeros_initializer()(shape=[self.bert_config.vocab_size]))

    def call(self, input_tensor, output_weights, positions, label_ids, label_weights):
        input_tensor = gather_indexes(input_tensor, positions)
        input_tensor = self.layer_dense(input_tensor)
        input_tensor = self.layer_norm(input_tensor)
        logits = tf.matmul(input_tensor, output_weights, transpose_b=True)
        logits = tf.nn.bias_add(logits, self.output_bias)
        log_probs = tf.nn.log_softmax(logits, axis=-1)
        label_ids = tf.reshape(label_ids, [-1])
        label_weights = tf.reshape(label_weights, [-1])

        one_hot_labels = tf.one_hot(
            label_ids, depth=self.bert_config.vocab_size, dtype=tf.float32)

        # The `positions` tensor might be zero-padded (if the sequence is too
        # short to have the maximum number of predictions). The `label_weights`
        # tensor has a value of 1.0 for every real prediction and 0.0 for the
        # padding predictions.
        # per_example_loss tensor shape is `[batch_size * seq_length]`
        per_example_loss = -tf.reduce_sum(log_probs * one_hot_labels, axis=[-1])
        numerator = tf.reduce_sum(label_weights * per_example_loss)
        denominator = tf.reduce_sum(label_weights) + 1e-5
        # loss tensor shape is `[]`
        loss = numerator / denominator

        return (loss, per_example_loss, log_probs)


def get_masked_lm_output(bert_config, input_tensor, output_weights, positions,
                         label_ids, label_weights):
    """Get loss and log probs for the masked LM."""
    """
        input_tensor: shape is `[batch_size, seq_length, hidden_size]`
        output_weights: shape is `[vocab_size, hidden_size]`
        position: shape is `[batch_size, seq_length]`
        label_ids: shape is `[batch_size, seq_length]`
        label_weights: shape is `[batch_size, seq_length]`
    """
    input_tensor = gather_indexes(input_tensor, positions)

    with tf.name_scope("cls/predictions"):
        # We apply one more non-linear transformation before the output layer.
        # This matrix is not used after pre-training.
        with tf.name_scope("transform"):
            input_tensor = tf.keras.layers.Dense(
                units=bert_config.hidden_size,
                activation=modeling.get_activation(bert_config.hidden_act),
                kernel_initializer=modeling.create_initializer(
                    bert_config.initializer_range))(input_tensor)
            input_tensor = modeling.layer_norm(input_tensor)

        # The output weights are the same as the input embeddings, but there is
        # an output-only bias for each token.
        output_bias = tf.Variable(
            name="output_bias",
            initial_value=tf.zeros_initializer()(shape=[bert_config.vocab_size]))
        logits = tf.matmul(input_tensor, output_weights, transpose_b=True)
        logits = tf.nn.bias_add(logits, output_bias)
        # log_probs tensor shape is `[batch_size * seq_length,  vocab_size]`
        log_probs = tf.nn.log_softmax(logits, axis=-1)

        label_ids = tf.reshape(label_ids, [-1])
        label_weights = tf.reshape(label_weights, [-1])

        one_hot_labels = tf.one_hot(
            label_ids, depth=bert_config.vocab_size, dtype=tf.float32)

        # The `positions` tensor might be zero-padded (if the sequence is too
        # short to have the maximum number of predictions). The `label_weights`
        # tensor has a value of 1.0 for every real prediction and 0.0 for the
        # padding predictions.
        # per_example_loss tensor shape is `[batch_size * seq_length]`
        per_example_loss = -tf.reduce_sum(log_probs * one_hot_labels, axis=[-1])
        numerator = tf.reduce_sum(label_weights * per_example_loss)
        denominator = tf.reduce_sum(label_weights) + 1e-5
        # loss tensor shape is `[]`
        loss = numerator / denominator

    return (loss, per_example_loss, log_probs)


class NextSentenceLayer(tf.keras.layers.Layer):

    def __init__(self, bert_config):
        super(NextSentenceLayer, self).__init__()
        self.bert_config = bert_config
        with tf.name_scope("cls/seq_relationship"):
            self.output_weights = tf.Variable(
                name="output_weights",
                initial_value=modeling.create_initializer(self.bert_config.initializer_range)(
                    shape=[2, self.bert_config.hidden_size])
            )

            self.output_bias = tf.Variable(
                name="output_bias",
                initial_value=tf.initializers.zeros()(shape=[2])
            )

    def call(self, input_tensor, labels):
        logits = tf.matmul(input_tensor, self.output_weights, transpose_b=True)
        logits = tf.nn.bias_add(logits, self.output_bias)
        log_probs = tf.nn.log_softmax(logits, axis=-1)
        labels = tf.reshape(labels, [-1])
        one_hot_labels = tf.one_hot(labels, depth=2, dtype=tf.float32)
        per_example_loss = -tf.reduce_sum(one_hot_labels * log_probs, axis=-1)
        loss = tf.reduce_mean(per_example_loss)
        # loss shape: [], per_example_loss shape [batch_size]
        # log_probs shape: [batch_size, 2]
        return (loss, per_example_loss, log_probs)


def get_next_sentence_output(bert_config, input_tensor, labels):
    """Get loss and log probs for the next sentence prediction."""
    """ bert_config: a BertConfig instance of BertConfig 
        input_tensor: shape is [batch_size, hidden_size] 
    """

    # Simple binary classification. Note that 0 is "next sentence" and 1 is
    # "random sentence". This weight matrix is not used after pre-training.
    with tf.name_scope("cls/seq_relationship"):
        output_weights = tf.Variable(
            name="output_weights",
            initial_value=modeling.create_initializer(bert_config.initializer_range)(shape=[2, bert_config.hidden_size])
        )
        """
        output_weights = tf.get_variable(
            "output_weights",
            shape=[2, bert_config.hidden_size],
            initializer=modeling.create_initializer(bert_config.initializer_range))
        """
        output_bias = tf.Variable(
            name="output_bias",
            initial_value=tf.initializers.zeros()(shape=[2])
        )
        """
        output_bias = tf.get_variable(
            "output_bias", shape=[2], initializer=tf.zeros_initializer())
        """
        logits = tf.matmul(input_tensor, output_weights, transpose_b=True)
        logits = tf.nn.bias_add(logits, output_bias)
        log_probs = tf.nn.log_softmax(logits, axis=-1)
        labels = tf.reshape(labels, [-1])
        one_hot_labels = tf.one_hot(labels, depth=2, dtype=tf.float32)
        per_example_loss = -tf.reduce_sum(one_hot_labels * log_probs, axis=-1)
        loss = tf.reduce_mean(per_example_loss)
        # loss shape: [], per_example_loss shape [batch_size]
        # log_probs shape: [batch_size, 2]
        return (loss, per_example_loss, log_probs)


def gather_indexes(sequence_tensor, positions):
    """Gathers the vectors at the specific positions over a minibatch."""
    sequence_shape = modeling.get_shape_list(sequence_tensor, expected_rank=3)
    batch_size = sequence_shape[0]
    seq_length = sequence_shape[1]
    width = sequence_shape[2]

    flat_offsets = tf.reshape(
        tf.range(0, batch_size, dtype=tf.int32) * seq_length, [-1, 1])
    flat_positions = tf.reshape(positions + flat_offsets, [-1])
    flat_sequence_tensor = tf.reshape(sequence_tensor,
                                      [batch_size * seq_length, width])
    output_tensor = tf.gather(flat_sequence_tensor, flat_positions)
    return output_tensor


def input_fn_builder(input_files,
                     max_seq_length,
                     max_predictions_per_seq,
                     is_training,
                     num_cpu_threads=4):
    """Creates an `input_fn` closure to be passed to TPUEstimator."""

    def input_fn(params):
        """The actual input function."""
        batch_size = params["batch_size"]

        name_to_features = {
            "input_ids":
                tf.io.FixedLenFeature([max_seq_length], tf.int64),
            "input_mask":
                tf.io.FixedLenFeature([max_seq_length], tf.int64),
            "segment_ids":
                tf.io.FixedLenFeature([max_seq_length], tf.int64),
            "masked_lm_positions":
                tf.io.FixedLenFeature([max_predictions_per_seq], tf.int64),
            "masked_lm_ids":
                tf.io.FixedLenFeature([max_predictions_per_seq], tf.int64),
            "masked_lm_weights":
                tf.io.FixedLenFeature([max_predictions_per_seq], tf.float32),
            "next_sentence_labels":
                tf.io.FixedLenFeature([1], tf.int64),
        }

        # For training, we want a lot of parallel reading and shuffling.
        # For eval, we want no shuffling and parallel reading doesn't matter.
        if is_training:
            d = tf.data.Dataset.from_tensor_slices(tf.constant(input_files))
            d = d.repeat()
            d = d.shuffle(buffer_size=len(input_files))

            # `cycle_length` is the number of parallel files that get read.
            cycle_length = min(num_cpu_threads, len(input_files))

            # `sloppy` mode means that the interleaving is not exact. This adds
            # even more randomness to the training pipeline.
            d = d.apply(
                tf.data.experimental.parallel_interleave(
                    tf.data.TFRecordDataset,
                    sloppy=is_training,
                    cycle_length=cycle_length))
            d = d.shuffle(buffer_size=100)
        else:
            d = tf.data.TFRecordDataset(input_files)
            # Since we evaluate for a fixed number of steps we don't want to encounter
            # out-of-range exceptions.
            d = d.repeat()

        # We must `drop_remainder` on training because the TPU requires fixed
        # size dimensions. For eval, we assume we are evaluating on the CPU or GPU
        # and we *don't* want to drop the remainder, otherwise we wont cover
        # every sample.
        d = d.apply(
            tf.data.experimental.map_and_batch(
                lambda record: _decode_record(record, name_to_features),
                batch_size=batch_size,
                num_parallel_batches=num_cpu_threads,
                drop_remainder=True))
        return d

    return input_fn


def _decode_record(record, name_to_features):
    """Decodes a record to a TensorFlow example."""
    example = tf.io.parse_single_example(record, name_to_features)

    # tf.Example only supports tf.int64, but the TPU only supports tf.int32.
    # So cast all int64 to int32.
    for name in list(example.keys()):
        t = example[name]
        if t.dtype == tf.int64:
            t = tf.dtypes.cast(t, tf.int32)
        example[name] = t

    return example


def main(_):
    tf.get_logger().setLevel(logging.INFO)

    if not FLAGS.do_train and not FLAGS.do_eval:
        raise ValueError("At least one of `do_train` or `do_eval` must be True.")

    bert_config = modeling.BertConfig.from_json_file(FLAGS.bert_config_file)

    tf.io.gfile.makedirs(FLAGS.output_dir)

    input_files = []
    for input_pattern in FLAGS.input_file.split(","):
        input_files.extend(tf.io.gfile.glob(input_pattern))

    tf.get_logger().info("*** Input Files ***")
    for input_file in input_files:
        tf.get_logger().info("  %s" % input_file)

    tpu_cluster_resolver = None
    if FLAGS.use_tpu and FLAGS.tpu_name:
        tpu_cluster_resolver = tf.contrib.cluster_resolver.TPUClusterResolver(
            FLAGS.tpu_name, zone=FLAGS.tpu_zone, project=FLAGS.gcp_project)

    is_per_host = tf.contrib.tpu.InputPipelineConfig.PER_HOST_V2
    run_config = tf.contrib.tpu.RunConfig(
        cluster=tpu_cluster_resolver,
        master=FLAGS.master,
        model_dir=FLAGS.output_dir,
        save_checkpoints_steps=FLAGS.save_checkpoints_steps,
        tpu_config=tf.contrib.tpu.TPUConfig(
            iterations_per_loop=FLAGS.iterations_per_loop,
            num_shards=FLAGS.num_tpu_cores,
            per_host_input_for_training=is_per_host))

    model_fn = model_fn_builder(
        bert_config=bert_config,
        init_checkpoint=FLAGS.init_checkpoint,
        learning_rate=FLAGS.learning_rate,
        num_train_steps=FLAGS.num_train_steps,
        num_warmup_steps=FLAGS.num_warmup_steps,
        use_tpu=FLAGS.use_tpu,
        use_one_hot_embeddings=FLAGS.use_tpu)

    # If TPU is not available, this will fall back to normal Estimator on CPU
    # or GPU.
    estimator = tf.contrib.tpu.TPUEstimator(
        use_tpu=FLAGS.use_tpu,
        model_fn=model_fn,
        config=run_config,
        train_batch_size=FLAGS.train_batch_size,
        eval_batch_size=FLAGS.eval_batch_size)

    if FLAGS.do_train:
        tf.get_logger().info("***** Running training *****")
        tf.get_logger().info("  Batch size = %d", FLAGS.train_batch_size)
        train_input_fn = input_fn_builder(
            input_files=input_files,
            max_seq_length=FLAGS.max_seq_length,
            max_predictions_per_seq=FLAGS.max_predictions_per_seq,
            is_training=True)
        estimator.train(input_fn=train_input_fn, max_steps=FLAGS.num_train_steps)

    if FLAGS.do_eval:
        tf.get_logger().info("***** Running evaluation *****")
        tf.get_logger().info("  Batch size = %d", FLAGS.eval_batch_size)

        eval_input_fn = input_fn_builder(
            input_files=input_files,
            max_seq_length=FLAGS.max_seq_length,
            max_predictions_per_seq=FLAGS.max_predictions_per_seq,
            is_training=False)

        result = estimator.evaluate(
            input_fn=eval_input_fn, steps=FLAGS.max_eval_steps)

        output_eval_file = os.path.join(FLAGS.output_dir, "eval_results.txt")
        with tf.io.gfile.GFile(output_eval_file, "w") as writer:
            tf.get_logger().info("***** Eval results *****")
            for key in sorted(result.keys()):
                tf.get_logger().info("  %s = %s", key, str(result[key]))
                writer.write("%s = %s\n" % (key, str(result[key])))


if __name__ == "__main__":
    flags.mark_flag_as_required("input_file")
    flags.mark_flag_as_required("bert_config_file")
    flags.mark_flag_as_required("output_dir")
    app.run()
