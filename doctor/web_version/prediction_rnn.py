import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn
from .util import convert_s_to_picture_com



def prediction(s):

    def RNN(x, weights, biases):
        # Prepare data shape to match `rnn` function requirements
        # Current data input shape: (batch_size, timesteps, n_input)
        # Required shape: 'timesteps' tensors list of shape (batch_size, n_input)

        # Unstack to get a list of 'timesteps' tensors of shape (batch_size, n_input)
        x = tf.unstack(x, timesteps, 1)

        # Define a lstm cell with tensorflow
        lstm_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=0.3)

        # Get lstm cell output
        outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

        # Linear activation, using rnn inner loop last output
        return tf.matmul(outputs[-1], weights['out']) + biases['out']

    def read_label_names(fn_label_names):
        label_names = np.load(fn_label_names)
        label_names = list(label_names)
        print(label_names)
        return label_names

    p_width, p_height = 26, 16 * 14 // 4
    input_width = (p_width * p_height) // 14
    label_len = 9

    num_input = input_width  # MNIST data input (img shape: 28*28)
    timesteps = 14  # timesteps
    num_hidden = 2 ** 11  # hidden layer num of features
    num_classes = label_len  # MNIST total classes (0-9 digits)

    # tf Graph input
    X = tf.placeholder(tf.float32, [None, timesteps, num_input])

    # Define weights
    weights = {
        'out': tf.Variable(tf.random_normal([num_hidden, num_classes]))
    }
    biases = {
        'out': tf.Variable(tf.random_normal([num_classes]))
    }

    logits = RNN(X, weights, biases)
    prediction = tf.nn.softmax(logits)
    answer = ""

    ### Saver
    saver = tf.train.Saver()

    # Start training
    with tf.Session() as sess:
        # store_path = '/home/b04901081/BM/models/model_rnn_2.ckpt'
        store_path = "/home/andy/桌面/BE/doctor/models/model_rnn_a_3.ckpt"
        saver.restore(sess, store_path)

        x_encoded = convert_s_to_picture_com(s)
        x = np.array([x_encoded])
        x = x.reshape(-1, 14, input_width)
        fn_label_names = "/home/andy/桌面/BE/doctor/label_names_9.npy"
        label_names = read_label_names(fn_label_names)
        y_pred = sess.run([prediction], feed_dict={X: x})
        y_pred = np.array(y_pred[0])
        prob = np.argwhere(y_pred > 0.35)
        if len(prob) > 0 :
            answer = label_names[y_pred.argmax()]
        else :
            answer = None
    return answer