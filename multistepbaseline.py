import tensorflow as tf

class MultiStepLastBaseline(tf.keras.Model):
    def call(self, inputs, OUT_STEPS=24):
        return tf.tile(inputs[:, -1:, :], [1, OUT_STEPS, 1])

