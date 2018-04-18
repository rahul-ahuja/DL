{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "collapsed": true
   },
   "source": [
    "# Language Translation\n",
    "In this project, you’re going to take a peek into the realm of neural network machine translation.  You’ll be training a sequence to sequence model on a dataset of English and French sentences that can translate new sentences from English to French.\n",
    "## Get the Data\n",
    "Since translating the whole language of English to French will take lots of time to train, we have provided you with a small portion of the English corpus."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL\n",
    "\"\"\"\n",
    "import helper\n",
    "import problem_unittests as tests\n",
    "\n",
    "source_path = 'data/small_vocab_en'\n",
    "target_path = 'data/small_vocab_fr'\n",
    "source_text = helper.load_data(source_path)\n",
    "target_text = helper.load_data(target_path)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Explore the Data\n",
    "Play around with view_sentence_range to view different parts of the data."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Dataset Stats\n",
      "Roughly the number of unique words: 227\n",
      "Number of sentences: 137861\n",
      "Average number of words in a sentence: 13.225277634719028\n",
      "\n",
      "English sentences 0 to 10:\n",
      "new jersey is sometimes quiet during autumn , and it is snowy in april .\n",
      "the united states is usually chilly during july , and it is usually freezing in november .\n",
      "california is usually quiet during march , and it is usually hot in june .\n",
      "the united states is sometimes mild during june , and it is cold in september .\n",
      "your least liked fruit is the grape , but my least liked is the apple .\n",
      "his favorite fruit is the orange , but my favorite is the grape .\n",
      "paris is relaxing during december , but it is usually chilly in july .\n",
      "new jersey is busy during spring , and it is never hot in march .\n",
      "our least liked fruit is the lemon , but my least liked is the grape .\n",
      "the united states is sometimes busy during january , and it is sometimes warm in november .\n",
      "\n",
      "French sentences 0 to 10:\n",
      "new jersey est parfois calme pendant l' automne , et il est neigeux en avril .\n",
      "les états-unis est généralement froid en juillet , et il gèle habituellement en novembre .\n",
      "california est généralement calme en mars , et il est généralement chaud en juin .\n",
      "les états-unis est parfois légère en juin , et il fait froid en septembre .\n",
      "votre moins aimé fruit est le raisin , mais mon moins aimé est la pomme .\n",
      "son fruit préféré est l'orange , mais mon préféré est le raisin .\n",
      "paris est relaxant en décembre , mais il est généralement froid en juillet .\n",
      "new jersey est occupé au printemps , et il est jamais chaude en mars .\n",
      "notre fruit est moins aimé le citron , mais mon moins aimé est le raisin .\n",
      "les états-unis est parfois occupé en janvier , et il est parfois chaud en novembre .\n"
     ]
    }
   ],
   "source": [
    "view_sentence_range = (0, 10)\n",
    "\n",
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL\n",
    "\"\"\"\n",
    "import numpy as np\n",
    "\n",
    "print('Dataset Stats')\n",
    "print('Roughly the number of unique words: {}'.format(len({word: None for word in source_text.split()})))\n",
    "\n",
    "sentences = source_text.split('\\n')\n",
    "word_counts = [len(sentence.split()) for sentence in sentences]\n",
    "print('Number of sentences: {}'.format(len(sentences)))\n",
    "print('Average number of words in a sentence: {}'.format(np.average(word_counts)))\n",
    "\n",
    "print()\n",
    "print('English sentences {} to {}:'.format(*view_sentence_range))\n",
    "print('\\n'.join(source_text.split('\\n')[view_sentence_range[0]:view_sentence_range[1]]))\n",
    "print()\n",
    "print('French sentences {} to {}:'.format(*view_sentence_range))\n",
    "print('\\n'.join(target_text.split('\\n')[view_sentence_range[0]:view_sentence_range[1]]))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Implement Preprocessing Function\n",
    "### Text to Word Ids\n",
    "As you did with other RNNs, you must turn the text into a number so the computer can understand it. In the function `text_to_ids()`, you'll turn `source_text` and `target_text` from words to ids.  However, you need to add the `<EOS>` word id at the end of `target_text`.  This will help the neural network predict when the sentence should end.\n",
    "\n",
    "You can get the `<EOS>` word id by doing:\n",
    "```python\n",
    "target_vocab_to_int['<EOS>']\n",
    "```\n",
    "You can get other word ids using `source_vocab_to_int` and `target_vocab_to_int`."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tests Passed\n"
     ]
    }
   ],
   "source": [
    "def text_to_ids(source_text, target_text, source_vocab_to_int, target_vocab_to_int):\n",
    "    \"\"\"\n",
    "    Convert source and target text to proper word ids\n",
    "    :param source_text: String that contains all the source text.\n",
    "    :param target_text: String that contains all the target text.\n",
    "    :param source_vocab_to_int: Dictionary to go from the source words to an id\n",
    "    :param target_vocab_to_int: Dictionary to go from the target words to an id\n",
    "    :return: A tuple of lists (source_id_text, target_id_text)\n",
    "    \"\"\"\n",
    "    # TODO: Implement Function\n",
    "    source_sentences = source_text.split('\\n')\n",
    "    target_sentences = target_text.split('\\n')\n",
    "    i=0\n",
    "    while i < len(source_sentences):\n",
    "        sentence = source_sentences[i]\n",
    "        target_sentence = target_sentences[i]\n",
    "        sentence = sentence.split()  \n",
    "        target_sentence = target_sentence.split()\n",
    "        target_id_text= []\n",
    "        source_id_text = []\n",
    "        for each in sentence:\n",
    "            source_id_text.append(source_vocab_to_int[each])\n",
    "        for each in target_sentence:\n",
    "            target_id_text.append(target_vocab_to_int[each]) \n",
    "        target_id_text.append(target_vocab_to_int['<EOS>'])\n",
    "        source_sentences[i] = source_id_text\n",
    "        target_sentences[i] = target_id_text\n",
    "        i += 1\n",
    "    \n",
    "    #source = [source_vocab_to_int[w] for w in s.split(' ') if w != '']\n",
    "    \n",
    "    \n",
    "    source_id_text = source_sentences\n",
    "    target_id_text = target_sentences\n",
    "    return source_id_text, target_id_text\n",
    "\n",
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE\n",
    "\"\"\"\n",
    "tests.test_text_to_ids(text_to_ids)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Preprocess all the data and save it\n",
    "Running the code cell below will preprocess all the data and save it to file."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL\n",
    "\"\"\"\n",
    "helper.preprocess_and_save_data(source_path, target_path, text_to_ids)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Check Point\n",
    "This is your first checkpoint. If you ever decide to come back to this notebook or have to restart the notebook, you can start from here. The preprocessed data has been saved to disk."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL\n",
    "\"\"\"\n",
    "import numpy as np\n",
    "import helper\n",
    "import problem_unittests as tests\n",
    "\n",
    "(source_int_text, target_int_text), (source_vocab_to_int, target_vocab_to_int), _ = helper.load_preprocess()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Check the Version of TensorFlow and Access to GPU\n",
    "This will check to make sure you have the correct version of TensorFlow and access to a GPU"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "TensorFlow Version: 1.1.0\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/home/rahul/anaconda3/envs/py35/lib/python3.5/site-packages/ipykernel_launcher.py:15: UserWarning: No GPU found. Please use a GPU to train your neural network.\n",
      "  from ipykernel import kernelapp as app\n"
     ]
    }
   ],
   "source": [
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL\n",
    "\"\"\"\n",
    "from distutils.version import LooseVersion\n",
    "import warnings\n",
    "import tensorflow as tf\n",
    "from tensorflow.python.layers.core import Dense\n",
    "\n",
    "# Check TensorFlow Version\n",
    "assert LooseVersion(tf.__version__) >= LooseVersion('1.1'), 'Please use TensorFlow version 1.1 or newer'\n",
    "print('TensorFlow Version: {}'.format(tf.__version__))\n",
    "\n",
    "# Check for a GPU\n",
    "if not tf.test.gpu_device_name():\n",
    "    warnings.warn('No GPU found. Please use a GPU to train your neural network.')\n",
    "else:\n",
    "    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Build the Neural Network\n",
    "You'll build the components necessary to build a Sequence-to-Sequence model by implementing the following functions below:\n",
    "- `model_inputs`\n",
    "- `process_decoder_input`\n",
    "- `encoding_layer`\n",
    "- `decoding_layer_train`\n",
    "- `decoding_layer_infer`\n",
    "- `decoding_layer`\n",
    "- `seq2seq_model`\n",
    "\n",
    "### Input\n",
    "Implement the `model_inputs()` function to create TF Placeholders for the Neural Network. It should create the following placeholders:\n",
    "\n",
    "- Input text placeholder named \"input\" using the TF Placeholder name parameter with rank 2.\n",
    "- Targets placeholder with rank 2.\n",
    "- Learning rate placeholder with rank 0.\n",
    "- Keep probability placeholder named \"keep_prob\" using the TF Placeholder name parameter with rank 0.\n",
    "- Target sequence length placeholder named \"target_sequence_length\" with rank 1\n",
    "- Max target sequence length tensor named \"max_target_len\" getting its value from applying tf.reduce_max on the target_sequence_length placeholder. Rank 0.\n",
    "- Source sequence length placeholder named \"source_sequence_length\" with rank 1\n",
    "\n",
    "Return the placeholders in the following the tuple (input, targets, learning rate, keep probability, target sequence length, max target sequence length, source sequence length)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tests Passed\n"
     ]
    }
   ],
   "source": [
    "def model_inputs():\n",
    "    \"\"\"\n",
    "    Create TF Placeholders for input, targets, learning rate, and lengths of source and target sequences.\n",
    "    :return: Tuple (input, targets, learning rate, keep probability, target sequence length,\n",
    "    max target sequence length, source sequence length)\n",
    "    \"\"\"\n",
    "    # TODO: Implement Function\n",
    "    inputs = tf.placeholder(tf.int32, [None, None], name='input')\n",
    "    targets = tf.placeholder(tf.int32, [None, None], name='targets')\n",
    "    lr = tf.placeholder(tf.float32, name='learning_rate')\n",
    "    keep_probability = tf.placeholder(tf.float32, name='keep_prob')\n",
    "    target_sequence_length = tf.placeholder(tf.int32, [None,], name='target_sequence_length')\n",
    "    max_target_sequence_length = tf.reduce_max(target_sequence_length, name='max_target_len')\n",
    "    source_sequence_length = tf.placeholder(tf.int32, [None,], name='source_sequence_length')\n",
    "    \n",
    "    return (inputs, targets, lr, keep_probability, target_sequence_length,\n",
    "    max_target_sequence_length, source_sequence_length)\n",
    "\n",
    "\n",
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE\n",
    "\"\"\"\n",
    "tests.test_model_inputs(model_inputs)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Process Decoder Input\n",
    "Implement `process_decoder_input` by removing the last word id from each batch in `target_data` and concat the GO ID to the begining of each batch."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tests Passed\n"
     ]
    }
   ],
   "source": [
    "def process_decoder_input(target_data, target_vocab_to_int, batch_size):\n",
    "    \"\"\"\n",
    "    Preprocess target data for encoding\n",
    "    :param target_data: Target Placehoder\n",
    "    :param target_vocab_to_int: Dictionary to go from the target words to an id\n",
    "    :param batch_size: Batch Size\n",
    "    :return: Preprocessed target data\n",
    "    \"\"\"\n",
    "    # TODO: Implement Function\n",
    "    ending = tf.strided_slice(target_data, [0, 0], [batch_size, -1], [1, 1])\n",
    "    dec_input = tf.concat([tf.fill([batch_size, 1], target_vocab_to_int['<GO>']), ending], 1)\n",
    "    \n",
    "    return dec_input\n",
    "\n",
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE\n",
    "\"\"\"\n",
    "tests.test_process_encoding_input(process_decoder_input)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Encoding\n",
    "Implement `encoding_layer()` to create a Encoder RNN layer:\n",
    " * Embed the encoder input using [`tf.contrib.layers.embed_sequence`](https://www.tensorflow.org/api_docs/python/tf/contrib/layers/embed_sequence)\n",
    " * Construct a [stacked](https://github.com/tensorflow/tensorflow/blob/6947f65a374ebf29e74bb71e36fd82760056d82c/tensorflow/docs_src/tutorials/recurrent.md#stacking-multiple-lstms) [`tf.contrib.rnn.LSTMCell`](https://www.tensorflow.org/api_docs/python/tf/contrib/rnn/LSTMCell) wrapped in a [`tf.contrib.rnn.DropoutWrapper`](https://www.tensorflow.org/api_docs/python/tf/contrib/rnn/DropoutWrapper)\n",
    " * Pass cell and embedded input to [`tf.nn.dynamic_rnn()`](https://www.tensorflow.org/api_docs/python/tf/nn/dynamic_rnn)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "/home/rahul/anaconda3/envs/py35/lib/python3.5/site-packages/h5py/__init__.py:34: FutureWarning: Conversion of the second argument of issubdtype from `float` to `np.floating` is deprecated. In future, it will be treated as `np.float64 == np.dtype(float).type`.\n",
      "  from ._conv import register_converters as _register_converters\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tests Passed\n"
     ]
    }
   ],
   "source": [
    "from imp import reload\n",
    "reload(tests)\n",
    "\n",
    "def encoding_layer(rnn_inputs, rnn_size, num_layers, keep_prob, \n",
    "                   source_sequence_length, source_vocab_size, \n",
    "                   encoding_embedding_size):\n",
    "    \"\"\"\n",
    "    Create encoding layer\n",
    "    :param rnn_inputs: Inputs for the RNN\n",
    "    :param rnn_size: RNN Size\n",
    "    :param num_layers: Number of layers\n",
    "    :param keep_prob: Dropout keep probability\n",
    "    :param source_sequence_length: a list of the lengths of each sequence in the batch\n",
    "    :param source_vocab_size: vocabulary size of source data\n",
    "    :param encoding_embedding_size: embedding size of source data\n",
    "    :return: tuple (RNN output, RNN state)\n",
    "    \"\"\"\n",
    "    # TODO: Implement Function\n",
    "    enc_embed_input = tf.contrib.layers.embed_sequence(rnn_inputs, source_vocab_size, encoding_embedding_size)\n",
    "\n",
    "    def build_cell(rnn_size):\n",
    "        enc_cell = tf.contrib.rnn.LSTMCell(rnn_size,\n",
    "                                           initializer=tf.random_uniform_initializer(-0.1, 0.1, seed=2))\n",
    "        \n",
    "        enc_cell = tf.contrib.rnn.DropoutWrapper(enc_cell, output_keep_prob=1)\n",
    "        \n",
    "        return enc_cell\n",
    "\n",
    "    enc_cell = tf.contrib.rnn.MultiRNNCell([build_cell(rnn_size) for _ in range(num_layers)])\n",
    "    \n",
    "    enc_output, enc_state = tf.nn.dynamic_rnn(enc_cell, enc_embed_input, sequence_length=source_sequence_length, dtype=tf.float32)\n",
    "    \n",
    "    return enc_output, enc_state\n",
    "\n",
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE\n",
    "\"\"\"\n",
    "tests.test_encoding_layer(encoding_layer)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Decoding - Training\n",
    "Create a training decoding layer:\n",
    "* Create a [`tf.contrib.seq2seq.TrainingHelper`](https://www.tensorflow.org/api_docs/python/tf/contrib/seq2seq/TrainingHelper) \n",
    "* Create a [`tf.contrib.seq2seq.BasicDecoder`](https://www.tensorflow.org/api_docs/python/tf/contrib/seq2seq/BasicDecoder)\n",
    "* Obtain the decoder outputs from [`tf.contrib.seq2seq.dynamic_decode`](https://www.tensorflow.org/api_docs/python/tf/contrib/seq2seq/dynamic_decode)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tests Passed\n"
     ]
    }
   ],
   "source": [
    "\n",
    "def decoding_layer_train(encoder_state, dec_cell, dec_embed_input, \n",
    "                         target_sequence_length, max_summary_length, \n",
    "                         output_layer, keep_prob):\n",
    "    \"\"\"\n",
    "    Create a decoding layer for training\n",
    "    :param encoder_state: Encoder State\n",
    "    :param dec_cell: Decoder RNN Cell\n",
    "    :param dec_embed_input: Decoder embedded input\n",
    "    :param target_sequence_length: The lengths of each sequence in the target batch\n",
    "    :param max_summary_length: The length of the longest sequence in the batch\n",
    "    :param output_layer: Function to apply the output layer\n",
    "    :param keep_prob: Dropout keep probability\n",
    "    :return: BasicDecoderOutput containing training logits and sample_id\n",
    "    \"\"\"\n",
    "    # TODO: Implement Function\n",
    "    training_helper = tf.contrib.seq2seq.TrainingHelper(inputs=dec_embed_input,\n",
    "                                                            sequence_length=target_sequence_length,\n",
    "                                                            time_major=False)\n",
    "    \n",
    "    training_decoder = tf.contrib.seq2seq.BasicDecoder(dec_cell,\n",
    "                                                           training_helper,\n",
    "                                                           encoder_state,\n",
    "                                                           output_layer)\n",
    "    training_decoder_output = tf.contrib.seq2seq.dynamic_decode(training_decoder,\n",
    "                                                                       impute_finished=True,\n",
    "                                                                       maximum_iterations=max_summary_length)[0]\n",
    "    return training_decoder_output\n",
    "\n",
    "\n",
    "\n",
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE\n",
    "\"\"\"\n",
    "tests.test_decoding_layer_train(decoding_layer_train)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Decoding - Inference\n",
    "Create inference decoder:\n",
    "* Create a [`tf.contrib.seq2seq.GreedyEmbeddingHelper`](https://www.tensorflow.org/api_docs/python/tf/contrib/seq2seq/GreedyEmbeddingHelper)\n",
    "* Create a [`tf.contrib.seq2seq.BasicDecoder`](https://www.tensorflow.org/api_docs/python/tf/contrib/seq2seq/BasicDecoder)\n",
    "* Obtain the decoder outputs from [`tf.contrib.seq2seq.dynamic_decode`](https://www.tensorflow.org/api_docs/python/tf/contrib/seq2seq/dynamic_decode)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tests Passed\n"
     ]
    }
   ],
   "source": [
    "def decoding_layer_infer(encoder_state, dec_cell, dec_embeddings, start_of_sequence_id,\n",
    "                         end_of_sequence_id, max_target_sequence_length,\n",
    "                         vocab_size, output_layer, batch_size, keep_prob):\n",
    "    \"\"\"\n",
    "    Create a decoding layer for inference\n",
    "    :param encoder_state: Encoder state\n",
    "    :param dec_cell: Decoder RNN Cell\n",
    "    :param dec_embeddings: Decoder embeddings\n",
    "    :param start_of_sequence_id: GO ID\n",
    "    :param end_of_sequence_id: EOS Id\n",
    "    :param max_target_sequence_length: Maximum length of target sequences\n",
    "    :param vocab_size: Size of decoder/target vocabulary\n",
    "    :param decoding_scope: TenorFlow Variable Scope for decoding\n",
    "    :param output_layer: Function to apply the output layer\n",
    "    :param batch_size: Batch size\n",
    "    :param keep_prob: Dropout keep probability\n",
    "    :return: BasicDecoderOutput containing inference logits and sample_id\n",
    "    \"\"\"\n",
    "    # TODO: Implement Function\n",
    "    start_tokens = tf.tile(tf.constant([start_of_sequence_id], dtype=tf.int32), [batch_size], name='start_tokens')\n",
    "\n",
    "    inference_helper = tf.contrib.seq2seq.GreedyEmbeddingHelper(dec_embeddings,\n",
    "                                                                start_tokens,\n",
    "                                                                end_of_sequence_id)\n",
    "    \n",
    "    inference_decoder = tf.contrib.seq2seq.BasicDecoder(dec_cell,\n",
    "                                                        inference_helper,\n",
    "                                                        encoder_state,\n",
    "                                                        output_layer=output_layer)\n",
    "    \n",
    "    inference_decoder_output = tf.contrib.seq2seq.dynamic_decode(inference_decoder,\n",
    "                                                            impute_finished=True,\n",
    "                                                            maximum_iterations=max_target_sequence_length)[0]\n",
    "    \n",
    "    return inference_decoder_output\n",
    "\n",
    "\n",
    "\n",
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE\n",
    "\"\"\"\n",
    "tests.test_decoding_layer_infer(decoding_layer_infer)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Build the Decoding Layer\n",
    "Implement `decoding_layer()` to create a Decoder RNN layer.\n",
    "\n",
    "* Embed the target sequences\n",
    "* Construct the decoder LSTM cell (just like you constructed the encoder cell above)\n",
    "* Create an output layer to map the outputs of the decoder to the elements of our vocabulary\n",
    "* Use the your `decoding_layer_train(encoder_state, dec_cell, dec_embed_input, target_sequence_length, max_target_sequence_length, output_layer, keep_prob)` function to get the training logits.\n",
    "* Use your `decoding_layer_infer(encoder_state, dec_cell, dec_embeddings, start_of_sequence_id, end_of_sequence_id, max_target_sequence_length, vocab_size, output_layer, batch_size, keep_prob)` function to get the inference logits.\n",
    "\n",
    "Note: You'll need to use [tf.variable_scope](https://www.tensorflow.org/api_docs/python/tf/variable_scope) to share variables between training and inference."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tests Passed\n"
     ]
    }
   ],
   "source": [
    "def decoding_layer(dec_input, encoder_state,\n",
    "                   target_sequence_length, max_target_sequence_length,\n",
    "                   rnn_size,\n",
    "                   num_layers, target_vocab_to_int, target_vocab_size,\n",
    "                   batch_size, keep_prob, decoding_embedding_size):\n",
    "    \"\"\"\n",
    "    Create decoding layer\n",
    "    :param dec_input: Decoder input\n",
    "    :param encoder_state: Encoder state\n",
    "    :param target_sequence_length: The lengths of each sequence in the target batch\n",
    "    :param max_target_sequence_length: Maximum length of target sequences\n",
    "    :param rnn_size: RNN Size\n",
    "    :param num_layers: Number of layers\n",
    "    :param target_vocab_to_int: Dictionary to go from the target words to an id\n",
    "    :param target_vocab_size: Size of target vocabulary\n",
    "    :param batch_size: The size of the batch\n",
    "    :param keep_prob: Dropout keep probability\n",
    "    :param decoding_embedding_size: Decoding embedding size\n",
    "    :return: Tuple of (Training BasicDecoderOutput, Inference BasicDecoderOutput)\n",
    "    \"\"\"\n",
    "    # TODO: Implement Function\n",
    "    dec_embeddings = tf.Variable(tf.random_uniform([target_vocab_size, decoding_embedding_size]))\n",
    "    dec_embed_input = tf.nn.embedding_lookup(dec_embeddings, dec_input)\n",
    "    \n",
    "    \n",
    "    def build_cell(rnn_size):\n",
    "        dec_cell = tf.contrib.rnn.LSTMCell(rnn_size,\n",
    "                                           initializer=tf.random_uniform_initializer(-0.1, 0.1, seed=2))\n",
    "        dec_cell = tf.contrib.rnn.DropoutWrapper(dec_cell, output_keep_prob=keep_prob)\n",
    "        \n",
    "        return dec_cell\n",
    "\n",
    "    dec_cell = tf.contrib.rnn.MultiRNNCell([build_cell(rnn_size) for _ in range(num_layers)])\n",
    "    \n",
    "    \n",
    "    output_layer = Dense(target_vocab_size,\n",
    "                         kernel_initializer = tf.truncated_normal_initializer(mean = 0.0, stddev=0.1))\n",
    "    \n",
    "    with tf.variable_scope(\"decode\"):\n",
    "        training_decoder_output = decoding_layer_train(encoder_state, dec_cell, dec_embed_input, target_sequence_length, \n",
    "                             max_target_sequence_length, output_layer, keep_prob)\n",
    "    with tf.variable_scope(\"decode\", reuse=True):\n",
    "        inference_decoder_output = decoding_layer_infer(encoder_state, dec_cell, dec_embeddings, target_vocab_to_int['<GO>'], \n",
    "                                                        target_vocab_to_int['<EOS>'], max_target_sequence_length, \n",
    "                                                        target_vocab_size, output_layer, batch_size, keep_prob)\n",
    "    \n",
    "    return training_decoder_output, inference_decoder_output\n",
    "\n",
    "\n",
    "\n",
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE\n",
    "\"\"\"\n",
    "tests.test_decoding_layer(decoding_layer)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Build the Neural Network\n",
    "Apply the functions you implemented above to:\n",
    "\n",
    "- Encode the input using your `encoding_layer(rnn_inputs, rnn_size, num_layers, keep_prob,  source_sequence_length, source_vocab_size, encoding_embedding_size)`.\n",
    "- Process target data using your `process_decoder_input(target_data, target_vocab_to_int, batch_size)` function.\n",
    "- Decode the encoded input using your `decoding_layer(dec_input, enc_state, target_sequence_length, max_target_sentence_length, rnn_size, num_layers, target_vocab_to_int, target_vocab_size, batch_size, keep_prob, dec_embedding_size)` function."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tests Passed\n"
     ]
    }
   ],
   "source": [
    "def seq2seq_model(input_data, target_data, keep_prob, batch_size,\n",
    "                  source_sequence_length, target_sequence_length,\n",
    "                  max_target_sentence_length,\n",
    "                  source_vocab_size, target_vocab_size,\n",
    "                  enc_embedding_size, dec_embedding_size,\n",
    "                  rnn_size, num_layers, target_vocab_to_int):\n",
    "    \"\"\"\n",
    "    Build the Sequence-to-Sequence part of the neural network\n",
    "    :param input_data: Input placeholder\n",
    "    :param target_data: Target placeholder\n",
    "    :param keep_prob: Dropout keep probability placeholder\n",
    "    :param batch_size: Batch Size\n",
    "    :param source_sequence_length: Sequence Lengths of source sequences in the batch\n",
    "    :param target_sequence_length: Sequence Lengths of target sequences in the batch\n",
    "    :param source_vocab_size: Source vocabulary size\n",
    "    :param target_vocab_size: Target vocabulary size\n",
    "    :param enc_embedding_size: Decoder embedding size\n",
    "    :param dec_embedding_size: Encoder embedding size\n",
    "    :param rnn_size: RNN Size\n",
    "    :param num_layers: Number of layers\n",
    "    :param target_vocab_to_int: Dictionary to go from the target words to an id\n",
    "    :return: Tuple of (Training BasicDecoderOutput, Inference BasicDecoderOutput)\n",
    "    \"\"\"\n",
    "    # TODO: Implement Function\n",
    "    enc_output, enc_state = encoding_layer(input_data, rnn_size, num_layers, keep_prob,  \n",
    "                   source_sequence_length, source_vocab_size, enc_embedding_size)\n",
    "    \n",
    "    dec_input = process_decoder_input(target_data, target_vocab_to_int, batch_size)\n",
    "    \n",
    "    training_decoder_output, inference_decoder_output = decoding_layer(dec_input, enc_state, \n",
    "                                                            target_sequence_length, max_target_sentence_length,\n",
    "                                                            rnn_size, num_layers, target_vocab_to_int, \n",
    "                                                            target_vocab_size, batch_size, \n",
    "                                                            keep_prob, dec_embedding_size)\n",
    "    \n",
    "    \n",
    "    \n",
    "    return training_decoder_output, inference_decoder_output\n",
    "\n",
    "\n",
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE\n",
    "\"\"\"\n",
    "tests.test_seq2seq_model(seq2seq_model)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Neural Network Training\n",
    "### Hyperparameters\n",
    "Tune the following parameters:\n",
    "\n",
    "- Set `epochs` to the number of epochs.\n",
    "- Set `batch_size` to the batch size.\n",
    "- Set `rnn_size` to the size of the RNNs.\n",
    "- Set `num_layers` to the number of layers.\n",
    "- Set `encoding_embedding_size` to the size of the embedding for the encoder.\n",
    "- Set `decoding_embedding_size` to the size of the embedding for the decoder.\n",
    "- Set `learning_rate` to the learning rate.\n",
    "- Set `keep_probability` to the Dropout keep probability\n",
    "- Set `display_step` to state how many steps between each debug output statement"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "# Number of Epochs\n",
    "epochs = 5\n",
    "# Batch Size\n",
    "batch_size = 256\n",
    "# RNN Size\n",
    "rnn_size = 512\n",
    "# Number of Layers\n",
    "num_layers = 1\n",
    "# Embedding Size\n",
    "encoding_embedding_size = 256\n",
    "decoding_embedding_size = 256\n",
    "# Learning Rate\n",
    "learning_rate = 0.01\n",
    "# Dropout Keep Probability\n",
    "keep_probability = 0.5\n",
    "display_step = 10"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Build the Graph\n",
    "Build the graph using the neural network you implemented."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL\n",
    "\"\"\"\n",
    "save_path = 'checkpoints/dev'\n",
    "(source_int_text, target_int_text), (source_vocab_to_int, target_vocab_to_int), _ = helper.load_preprocess()\n",
    "max_target_sentence_length = max([len(sentence) for sentence in source_int_text])\n",
    "\n",
    "train_graph = tf.Graph()\n",
    "with train_graph.as_default():\n",
    "    input_data, targets, lr, keep_prob, target_sequence_length, max_target_sequence_length, source_sequence_length = model_inputs()\n",
    "\n",
    "    #sequence_length = tf.placeholder_with_default(max_target_sentence_length, None, name='sequence_length')\n",
    "    input_shape = tf.shape(input_data)\n",
    "\n",
    "    train_logits, inference_logits = seq2seq_model(tf.reverse(input_data, [-1]),\n",
    "                                                   targets,\n",
    "                                                   keep_prob,\n",
    "                                                   batch_size,\n",
    "                                                   source_sequence_length,\n",
    "                                                   target_sequence_length,\n",
    "                                                   max_target_sequence_length,\n",
    "                                                   len(source_vocab_to_int),\n",
    "                                                   len(target_vocab_to_int),\n",
    "                                                   encoding_embedding_size,\n",
    "                                                   decoding_embedding_size,\n",
    "                                                   rnn_size,\n",
    "                                                   num_layers,\n",
    "                                                   target_vocab_to_int)\n",
    "\n",
    "\n",
    "    training_logits = tf.identity(train_logits.rnn_output, name='logits')\n",
    "    inference_logits = tf.identity(inference_logits.sample_id, name='predictions')\n",
    "\n",
    "    masks = tf.sequence_mask(target_sequence_length, max_target_sequence_length, dtype=tf.float32, name='masks')\n",
    "\n",
    "    with tf.name_scope(\"optimization\"):\n",
    "        # Loss function\n",
    "        cost = tf.contrib.seq2seq.sequence_loss(\n",
    "            training_logits,\n",
    "            targets,\n",
    "            masks)\n",
    "\n",
    "        # Optimizer\n",
    "        optimizer = tf.train.AdamOptimizer(lr)\n",
    "\n",
    "        # Gradient Clipping\n",
    "        gradients = optimizer.compute_gradients(cost)\n",
    "        capped_gradients = [(tf.clip_by_value(grad, -1., 1.), var) for grad, var in gradients if grad is not None]\n",
    "        train_op = optimizer.apply_gradients(capped_gradients)\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Batch and pad the source and target sequences"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL\n",
    "\"\"\"\n",
    "def pad_sentence_batch(sentence_batch, pad_int):\n",
    "    \"\"\"Pad sentences with <PAD> so that each sentence of a batch has the same length\"\"\"\n",
    "    max_sentence = max([len(sentence) for sentence in sentence_batch])\n",
    "    return [sentence + [pad_int] * (max_sentence - len(sentence)) for sentence in sentence_batch]\n",
    "\n",
    "\n",
    "def get_batches(sources, targets, batch_size, source_pad_int, target_pad_int):\n",
    "    \"\"\"Batch targets, sources, and the lengths of their sentences together\"\"\"\n",
    "    for batch_i in range(0, len(sources)//batch_size):\n",
    "        start_i = batch_i * batch_size\n",
    "\n",
    "        # Slice the right amount for the batch\n",
    "        sources_batch = sources[start_i:start_i + batch_size]\n",
    "        targets_batch = targets[start_i:start_i + batch_size]\n",
    "\n",
    "        # Pad\n",
    "        pad_sources_batch = np.array(pad_sentence_batch(sources_batch, source_pad_int))\n",
    "        pad_targets_batch = np.array(pad_sentence_batch(targets_batch, target_pad_int))\n",
    "\n",
    "        # Need the lengths for the _lengths parameters\n",
    "        pad_targets_lengths = []\n",
    "        for target in pad_targets_batch:\n",
    "            pad_targets_lengths.append(len(target))\n",
    "\n",
    "        pad_source_lengths = []\n",
    "        for source in pad_sources_batch:\n",
    "            pad_source_lengths.append(len(source))\n",
    "\n",
    "        yield pad_sources_batch, pad_targets_batch, pad_source_lengths, pad_targets_lengths\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Train\n",
    "Train the neural network on the preprocessed data. If you have a hard time getting a good loss, check the forms to see if anyone is having the same problem."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch   0 Batch   10/538 - Train Accuracy: 0.2687, Validation Accuracy: 0.3535, Loss: 3.4802\n",
      "Epoch   0 Batch   20/538 - Train Accuracy: 0.3830, Validation Accuracy: 0.4171, Loss: 2.5589\n",
      "Epoch   0 Batch   30/538 - Train Accuracy: 0.3238, Validation Accuracy: 0.3867, Loss: 2.0935\n",
      "Epoch   0 Batch   40/538 - Train Accuracy: 0.4421, Validation Accuracy: 0.4318, Loss: 1.4244\n",
      "Epoch   0 Batch   50/538 - Train Accuracy: 0.4617, Validation Accuracy: 0.5018, Loss: 1.2489\n",
      "Epoch   0 Batch   60/538 - Train Accuracy: 0.4678, Validation Accuracy: 0.5073, Loss: 1.0900\n",
      "Epoch   0 Batch   70/538 - Train Accuracy: 0.4762, Validation Accuracy: 0.5108, Loss: 0.9727\n",
      "Epoch   0 Batch   80/538 - Train Accuracy: 0.4801, Validation Accuracy: 0.5231, Loss: 0.9555\n",
      "Epoch   0 Batch   90/538 - Train Accuracy: 0.5192, Validation Accuracy: 0.5433, Loss: 0.8660\n",
      "Epoch   0 Batch  100/538 - Train Accuracy: 0.5275, Validation Accuracy: 0.5375, Loss: 0.8191\n",
      "Epoch   0 Batch  110/538 - Train Accuracy: 0.5141, Validation Accuracy: 0.5558, Loss: 0.8062\n",
      "Epoch   0 Batch  120/538 - Train Accuracy: 0.5283, Validation Accuracy: 0.5542, Loss: 0.7577\n",
      "Epoch   0 Batch  130/538 - Train Accuracy: 0.5506, Validation Accuracy: 0.5581, Loss: 0.7219\n",
      "Epoch   0 Batch  140/538 - Train Accuracy: 0.5164, Validation Accuracy: 0.5661, Loss: 0.7708\n",
      "Epoch   0 Batch  150/538 - Train Accuracy: 0.5656, Validation Accuracy: 0.5708, Loss: 0.6940\n",
      "Epoch   0 Batch  160/538 - Train Accuracy: 0.5640, Validation Accuracy: 0.5730, Loss: 0.6589\n",
      "Epoch   0 Batch  170/538 - Train Accuracy: 0.5885, Validation Accuracy: 0.5891, Loss: 0.6602\n",
      "Epoch   0 Batch  180/538 - Train Accuracy: 0.5924, Validation Accuracy: 0.5906, Loss: 0.6222\n",
      "Epoch   0 Batch  190/538 - Train Accuracy: 0.5956, Validation Accuracy: 0.6069, Loss: 0.6281\n",
      "Epoch   0 Batch  200/538 - Train Accuracy: 0.5857, Validation Accuracy: 0.6003, Loss: 0.5941\n",
      "Epoch   0 Batch  210/538 - Train Accuracy: 0.6012, Validation Accuracy: 0.6088, Loss: 0.5916\n",
      "Epoch   0 Batch  220/538 - Train Accuracy: 0.5884, Validation Accuracy: 0.6040, Loss: 0.5679\n",
      "Epoch   0 Batch  230/538 - Train Accuracy: 0.6150, Validation Accuracy: 0.6314, Loss: 0.5763\n",
      "Epoch   0 Batch  240/538 - Train Accuracy: 0.6301, Validation Accuracy: 0.6431, Loss: 0.5561\n",
      "Epoch   0 Batch  250/538 - Train Accuracy: 0.6279, Validation Accuracy: 0.6323, Loss: 0.5389\n",
      "Epoch   0 Batch  260/538 - Train Accuracy: 0.6373, Validation Accuracy: 0.6436, Loss: 0.5200\n",
      "Epoch   0 Batch  270/538 - Train Accuracy: 0.6523, Validation Accuracy: 0.6502, Loss: 0.5229\n",
      "Epoch   0 Batch  280/538 - Train Accuracy: 0.6975, Validation Accuracy: 0.6507, Loss: 0.4749\n",
      "Epoch   0 Batch  290/538 - Train Accuracy: 0.6586, Validation Accuracy: 0.6703, Loss: 0.4824\n",
      "Epoch   0 Batch  300/538 - Train Accuracy: 0.6892, Validation Accuracy: 0.6676, Loss: 0.4644\n",
      "Epoch   0 Batch  310/538 - Train Accuracy: 0.7021, Validation Accuracy: 0.6861, Loss: 0.4686\n",
      "Epoch   0 Batch  320/538 - Train Accuracy: 0.6815, Validation Accuracy: 0.6667, Loss: 0.4461\n",
      "Epoch   0 Batch  330/538 - Train Accuracy: 0.6750, Validation Accuracy: 0.6708, Loss: 0.4175\n",
      "Epoch   0 Batch  340/538 - Train Accuracy: 0.6727, Validation Accuracy: 0.6964, Loss: 0.4330\n",
      "Epoch   0 Batch  350/538 - Train Accuracy: 0.7165, Validation Accuracy: 0.6912, Loss: 0.4149\n",
      "Epoch   0 Batch  360/538 - Train Accuracy: 0.7043, Validation Accuracy: 0.7079, Loss: 0.4013\n",
      "Epoch   0 Batch  370/538 - Train Accuracy: 0.7109, Validation Accuracy: 0.7172, Loss: 0.4102\n",
      "Epoch   0 Batch  380/538 - Train Accuracy: 0.7260, Validation Accuracy: 0.7212, Loss: 0.3720\n",
      "Epoch   0 Batch  390/538 - Train Accuracy: 0.7535, Validation Accuracy: 0.7466, Loss: 0.3517\n",
      "Epoch   0 Batch  400/538 - Train Accuracy: 0.7379, Validation Accuracy: 0.7440, Loss: 0.3515\n",
      "Epoch   0 Batch  410/538 - Train Accuracy: 0.7377, Validation Accuracy: 0.7383, Loss: 0.3412\n",
      "Epoch   0 Batch  420/538 - Train Accuracy: 0.7627, Validation Accuracy: 0.7496, Loss: 0.3452\n",
      "Epoch   0 Batch  430/538 - Train Accuracy: 0.7463, Validation Accuracy: 0.7489, Loss: 0.3148\n",
      "Epoch   0 Batch  440/538 - Train Accuracy: 0.7465, Validation Accuracy: 0.7475, Loss: 0.3287\n",
      "Epoch   0 Batch  450/538 - Train Accuracy: 0.7693, Validation Accuracy: 0.7708, Loss: 0.3097\n",
      "Epoch   0 Batch  460/538 - Train Accuracy: 0.7522, Validation Accuracy: 0.7765, Loss: 0.2932\n",
      "Epoch   0 Batch  470/538 - Train Accuracy: 0.7863, Validation Accuracy: 0.7955, Loss: 0.2718\n",
      "Epoch   0 Batch  480/538 - Train Accuracy: 0.7919, Validation Accuracy: 0.7731, Loss: 0.2661\n",
      "Epoch   0 Batch  490/538 - Train Accuracy: 0.7803, Validation Accuracy: 0.8031, Loss: 0.2541\n",
      "Epoch   0 Batch  500/538 - Train Accuracy: 0.8178, Validation Accuracy: 0.7951, Loss: 0.2331\n",
      "Epoch   0 Batch  510/538 - Train Accuracy: 0.7881, Validation Accuracy: 0.8054, Loss: 0.2426\n",
      "Epoch   0 Batch  520/538 - Train Accuracy: 0.7973, Validation Accuracy: 0.7995, Loss: 0.2492\n",
      "Epoch   0 Batch  530/538 - Train Accuracy: 0.7994, Validation Accuracy: 0.8102, Loss: 0.2325\n",
      "Epoch   1 Batch   10/538 - Train Accuracy: 0.7988, Validation Accuracy: 0.7900, Loss: 0.2262\n",
      "Epoch   1 Batch   20/538 - Train Accuracy: 0.8451, Validation Accuracy: 0.8139, Loss: 0.2111\n",
      "Epoch   1 Batch   30/538 - Train Accuracy: 0.8113, Validation Accuracy: 0.8173, Loss: 0.2032\n",
      "Epoch   1 Batch   40/538 - Train Accuracy: 0.8663, Validation Accuracy: 0.8281, Loss: 0.1646\n",
      "Epoch   1 Batch   50/538 - Train Accuracy: 0.8496, Validation Accuracy: 0.8161, Loss: 0.1799\n",
      "Epoch   1 Batch   60/538 - Train Accuracy: 0.8471, Validation Accuracy: 0.8423, Loss: 0.1856\n",
      "Epoch   1 Batch   70/538 - Train Accuracy: 0.8445, Validation Accuracy: 0.8322, Loss: 0.1695\n",
      "Epoch   1 Batch   80/538 - Train Accuracy: 0.8578, Validation Accuracy: 0.8207, Loss: 0.1702\n",
      "Epoch   1 Batch   90/538 - Train Accuracy: 0.8363, Validation Accuracy: 0.8349, Loss: 0.1871\n",
      "Epoch   1 Batch  100/538 - Train Accuracy: 0.8801, Validation Accuracy: 0.8530, Loss: 0.1551\n",
      "Epoch   1 Batch  110/538 - Train Accuracy: 0.8594, Validation Accuracy: 0.8530, Loss: 0.1651\n",
      "Epoch   1 Batch  120/538 - Train Accuracy: 0.8936, Validation Accuracy: 0.8565, Loss: 0.1368\n",
      "Epoch   1 Batch  130/538 - Train Accuracy: 0.8806, Validation Accuracy: 0.8542, Loss: 0.1405\n",
      "Epoch   1 Batch  140/538 - Train Accuracy: 0.8484, Validation Accuracy: 0.8647, Loss: 0.1602\n",
      "Epoch   1 Batch  150/538 - Train Accuracy: 0.8744, Validation Accuracy: 0.8532, Loss: 0.1308\n",
      "Epoch   1 Batch  160/538 - Train Accuracy: 0.8650, Validation Accuracy: 0.8565, Loss: 0.1162\n",
      "Epoch   1 Batch  170/538 - Train Accuracy: 0.8744, Validation Accuracy: 0.8622, Loss: 0.1316\n",
      "Epoch   1 Batch  180/538 - Train Accuracy: 0.8930, Validation Accuracy: 0.8532, Loss: 0.1322\n",
      "Epoch   1 Batch  190/538 - Train Accuracy: 0.8683, Validation Accuracy: 0.8663, Loss: 0.1468\n",
      "Epoch   1 Batch  200/538 - Train Accuracy: 0.8664, Validation Accuracy: 0.8592, Loss: 0.1096\n",
      "Epoch   1 Batch  210/538 - Train Accuracy: 0.8644, Validation Accuracy: 0.8874, Loss: 0.1212\n",
      "Epoch   1 Batch  220/538 - Train Accuracy: 0.8737, Validation Accuracy: 0.8711, Loss: 0.1156\n",
      "Epoch   1 Batch  230/538 - Train Accuracy: 0.8902, Validation Accuracy: 0.8674, Loss: 0.1187\n",
      "Epoch   1 Batch  240/538 - Train Accuracy: 0.8627, Validation Accuracy: 0.8862, Loss: 0.1145\n",
      "Epoch   1 Batch  250/538 - Train Accuracy: 0.8963, Validation Accuracy: 0.8920, Loss: 0.1154\n",
      "Epoch   1 Batch  260/538 - Train Accuracy: 0.8562, Validation Accuracy: 0.8691, Loss: 0.1083\n",
      "Epoch   1 Batch  270/538 - Train Accuracy: 0.8982, Validation Accuracy: 0.8725, Loss: 0.1151\n",
      "Epoch   1 Batch  280/538 - Train Accuracy: 0.8690, Validation Accuracy: 0.8794, Loss: 0.1049\n",
      "Epoch   1 Batch  290/538 - Train Accuracy: 0.8830, Validation Accuracy: 0.8663, Loss: 0.1019\n",
      "Epoch   1 Batch  300/538 - Train Accuracy: 0.8901, Validation Accuracy: 0.8988, Loss: 0.1058\n",
      "Epoch   1 Batch  310/538 - Train Accuracy: 0.9232, Validation Accuracy: 0.8768, Loss: 0.0993\n",
      "Epoch   1 Batch  320/538 - Train Accuracy: 0.8940, Validation Accuracy: 0.8970, Loss: 0.0849\n",
      "Epoch   1 Batch  330/538 - Train Accuracy: 0.9163, Validation Accuracy: 0.9027, Loss: 0.0894\n",
      "Epoch   1 Batch  340/538 - Train Accuracy: 0.8799, Validation Accuracy: 0.8972, Loss: 0.0959\n",
      "Epoch   1 Batch  350/538 - Train Accuracy: 0.9025, Validation Accuracy: 0.8967, Loss: 0.0992\n",
      "Epoch   1 Batch  360/538 - Train Accuracy: 0.9178, Validation Accuracy: 0.9007, Loss: 0.0953\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch   1 Batch  370/538 - Train Accuracy: 0.9150, Validation Accuracy: 0.8983, Loss: 0.0935\n",
      "Epoch   1 Batch  380/538 - Train Accuracy: 0.9084, Validation Accuracy: 0.9135, Loss: 0.0863\n",
      "Epoch   1 Batch  390/538 - Train Accuracy: 0.9425, Validation Accuracy: 0.9052, Loss: 0.0780\n",
      "Epoch   1 Batch  400/538 - Train Accuracy: 0.9172, Validation Accuracy: 0.9165, Loss: 0.0859\n",
      "Epoch   1 Batch  410/538 - Train Accuracy: 0.9328, Validation Accuracy: 0.9009, Loss: 0.0870\n",
      "Epoch   1 Batch  420/538 - Train Accuracy: 0.9262, Validation Accuracy: 0.9245, Loss: 0.0738\n",
      "Epoch   1 Batch  430/538 - Train Accuracy: 0.9072, Validation Accuracy: 0.9015, Loss: 0.0766\n",
      "Epoch   1 Batch  440/538 - Train Accuracy: 0.9168, Validation Accuracy: 0.9134, Loss: 0.0966\n",
      "Epoch   1 Batch  450/538 - Train Accuracy: 0.8956, Validation Accuracy: 0.9164, Loss: 0.0925\n",
      "Epoch   1 Batch  460/538 - Train Accuracy: 0.9003, Validation Accuracy: 0.9061, Loss: 0.0883\n",
      "Epoch   1 Batch  470/538 - Train Accuracy: 0.9222, Validation Accuracy: 0.9190, Loss: 0.0804\n",
      "Epoch   1 Batch  480/538 - Train Accuracy: 0.9053, Validation Accuracy: 0.9103, Loss: 0.0752\n",
      "Epoch   1 Batch  490/538 - Train Accuracy: 0.9198, Validation Accuracy: 0.9086, Loss: 0.0662\n",
      "Epoch   1 Batch  500/538 - Train Accuracy: 0.9412, Validation Accuracy: 0.8945, Loss: 0.0583\n",
      "Epoch   1 Batch  510/538 - Train Accuracy: 0.9249, Validation Accuracy: 0.9022, Loss: 0.0704\n",
      "Epoch   1 Batch  520/538 - Train Accuracy: 0.9041, Validation Accuracy: 0.9110, Loss: 0.0798\n",
      "Epoch   1 Batch  530/538 - Train Accuracy: 0.8986, Validation Accuracy: 0.9116, Loss: 0.0829\n",
      "Epoch   2 Batch   10/538 - Train Accuracy: 0.8922, Validation Accuracy: 0.9112, Loss: 0.0838\n",
      "Epoch   2 Batch   20/538 - Train Accuracy: 0.9208, Validation Accuracy: 0.9128, Loss: 0.0802\n",
      "Epoch   2 Batch   30/538 - Train Accuracy: 0.9023, Validation Accuracy: 0.9132, Loss: 0.0786\n",
      "Epoch   2 Batch   40/538 - Train Accuracy: 0.9281, Validation Accuracy: 0.9160, Loss: 0.0637\n",
      "Epoch   2 Batch   50/538 - Train Accuracy: 0.9057, Validation Accuracy: 0.9309, Loss: 0.0628\n",
      "Epoch   2 Batch   60/538 - Train Accuracy: 0.9355, Validation Accuracy: 0.9018, Loss: 0.0665\n",
      "Epoch   2 Batch   70/538 - Train Accuracy: 0.9247, Validation Accuracy: 0.9034, Loss: 0.0594\n",
      "Epoch   2 Batch   80/538 - Train Accuracy: 0.9281, Validation Accuracy: 0.9091, Loss: 0.0675\n",
      "Epoch   2 Batch   90/538 - Train Accuracy: 0.9051, Validation Accuracy: 0.9173, Loss: 0.0799\n",
      "Epoch   2 Batch  100/538 - Train Accuracy: 0.9418, Validation Accuracy: 0.9181, Loss: 0.0661\n",
      "Epoch   2 Batch  110/538 - Train Accuracy: 0.9156, Validation Accuracy: 0.9228, Loss: 0.0662\n",
      "Epoch   2 Batch  120/538 - Train Accuracy: 0.9385, Validation Accuracy: 0.9183, Loss: 0.0566\n",
      "Epoch   2 Batch  130/538 - Train Accuracy: 0.9263, Validation Accuracy: 0.9268, Loss: 0.0639\n",
      "Epoch   2 Batch  140/538 - Train Accuracy: 0.9234, Validation Accuracy: 0.9183, Loss: 0.0871\n",
      "Epoch   2 Batch  150/538 - Train Accuracy: 0.9357, Validation Accuracy: 0.9142, Loss: 0.0580\n",
      "Epoch   2 Batch  160/538 - Train Accuracy: 0.9243, Validation Accuracy: 0.9173, Loss: 0.0587\n",
      "Epoch   2 Batch  170/538 - Train Accuracy: 0.9096, Validation Accuracy: 0.9213, Loss: 0.0674\n",
      "Epoch   2 Batch  180/538 - Train Accuracy: 0.9347, Validation Accuracy: 0.9249, Loss: 0.0704\n",
      "Epoch   2 Batch  190/538 - Train Accuracy: 0.9462, Validation Accuracy: 0.9158, Loss: 0.0754\n",
      "Epoch   2 Batch  200/538 - Train Accuracy: 0.9326, Validation Accuracy: 0.9098, Loss: 0.0536\n",
      "Epoch   2 Batch  210/538 - Train Accuracy: 0.9102, Validation Accuracy: 0.9203, Loss: 0.0667\n",
      "Epoch   2 Batch  220/538 - Train Accuracy: 0.9195, Validation Accuracy: 0.9167, Loss: 0.0596\n",
      "Epoch   2 Batch  230/538 - Train Accuracy: 0.9260, Validation Accuracy: 0.9164, Loss: 0.0638\n",
      "Epoch   2 Batch  240/538 - Train Accuracy: 0.9332, Validation Accuracy: 0.9313, Loss: 0.0620\n",
      "Epoch   2 Batch  250/538 - Train Accuracy: 0.9342, Validation Accuracy: 0.9320, Loss: 0.0569\n",
      "Epoch   2 Batch  260/538 - Train Accuracy: 0.9027, Validation Accuracy: 0.9251, Loss: 0.0670\n",
      "Epoch   2 Batch  270/538 - Train Accuracy: 0.9391, Validation Accuracy: 0.9194, Loss: 0.0590\n",
      "Epoch   2 Batch  280/538 - Train Accuracy: 0.9461, Validation Accuracy: 0.9224, Loss: 0.0490\n",
      "Epoch   2 Batch  290/538 - Train Accuracy: 0.9445, Validation Accuracy: 0.9130, Loss: 0.0519\n",
      "Epoch   2 Batch  300/538 - Train Accuracy: 0.9308, Validation Accuracy: 0.9292, Loss: 0.0567\n",
      "Epoch   2 Batch  310/538 - Train Accuracy: 0.9516, Validation Accuracy: 0.9228, Loss: 0.0642\n",
      "Epoch   2 Batch  320/538 - Train Accuracy: 0.9338, Validation Accuracy: 0.9022, Loss: 0.0540\n",
      "Epoch   2 Batch  330/538 - Train Accuracy: 0.9399, Validation Accuracy: 0.9309, Loss: 0.0603\n",
      "Epoch   2 Batch  340/538 - Train Accuracy: 0.9334, Validation Accuracy: 0.9336, Loss: 0.0558\n",
      "Epoch   2 Batch  350/538 - Train Accuracy: 0.9364, Validation Accuracy: 0.8970, Loss: 0.0646\n",
      "Epoch   2 Batch  360/538 - Train Accuracy: 0.9521, Validation Accuracy: 0.9366, Loss: 0.0477\n",
      "Epoch   2 Batch  370/538 - Train Accuracy: 0.9383, Validation Accuracy: 0.9437, Loss: 0.0579\n",
      "Epoch   2 Batch  380/538 - Train Accuracy: 0.9512, Validation Accuracy: 0.9306, Loss: 0.0536\n",
      "Epoch   2 Batch  390/538 - Train Accuracy: 0.9364, Validation Accuracy: 0.9233, Loss: 0.0456\n",
      "Epoch   2 Batch  400/538 - Train Accuracy: 0.9360, Validation Accuracy: 0.9480, Loss: 0.0502\n",
      "Epoch   2 Batch  410/538 - Train Accuracy: 0.9527, Validation Accuracy: 0.9336, Loss: 0.0521\n",
      "Epoch   2 Batch  420/538 - Train Accuracy: 0.9662, Validation Accuracy: 0.9389, Loss: 0.0538\n",
      "Epoch   2 Batch  430/538 - Train Accuracy: 0.9328, Validation Accuracy: 0.9382, Loss: 0.0596\n",
      "Epoch   2 Batch  440/538 - Train Accuracy: 0.9391, Validation Accuracy: 0.9272, Loss: 0.0578\n",
      "Epoch   2 Batch  450/538 - Train Accuracy: 0.9310, Validation Accuracy: 0.9375, Loss: 0.0675\n",
      "Epoch   2 Batch  460/538 - Train Accuracy: 0.9232, Validation Accuracy: 0.9439, Loss: 0.0569\n",
      "Epoch   2 Batch  470/538 - Train Accuracy: 0.9436, Validation Accuracy: 0.9176, Loss: 0.0465\n",
      "Epoch   2 Batch  480/538 - Train Accuracy: 0.9529, Validation Accuracy: 0.9341, Loss: 0.0431\n",
      "Epoch   2 Batch  490/538 - Train Accuracy: 0.9498, Validation Accuracy: 0.9400, Loss: 0.0464\n",
      "Epoch   2 Batch  500/538 - Train Accuracy: 0.9627, Validation Accuracy: 0.9347, Loss: 0.0413\n",
      "Epoch   2 Batch  510/538 - Train Accuracy: 0.9580, Validation Accuracy: 0.9348, Loss: 0.0463\n",
      "Epoch   2 Batch  520/538 - Train Accuracy: 0.9295, Validation Accuracy: 0.9382, Loss: 0.0539\n",
      "Epoch   2 Batch  530/538 - Train Accuracy: 0.9342, Validation Accuracy: 0.9505, Loss: 0.0585\n",
      "Epoch   3 Batch   10/538 - Train Accuracy: 0.9207, Validation Accuracy: 0.9386, Loss: 0.0626\n",
      "Epoch   3 Batch   20/538 - Train Accuracy: 0.9431, Validation Accuracy: 0.9485, Loss: 0.0477\n",
      "Epoch   3 Batch   30/538 - Train Accuracy: 0.9328, Validation Accuracy: 0.9421, Loss: 0.0554\n",
      "Epoch   3 Batch   40/538 - Train Accuracy: 0.9389, Validation Accuracy: 0.9411, Loss: 0.0444\n",
      "Epoch   3 Batch   50/538 - Train Accuracy: 0.9365, Validation Accuracy: 0.9345, Loss: 0.0500\n",
      "Epoch   3 Batch   60/538 - Train Accuracy: 0.9414, Validation Accuracy: 0.9473, Loss: 0.0522\n",
      "Epoch   3 Batch   70/538 - Train Accuracy: 0.9442, Validation Accuracy: 0.9284, Loss: 0.0429\n",
      "Epoch   3 Batch   80/538 - Train Accuracy: 0.9414, Validation Accuracy: 0.9418, Loss: 0.0437\n",
      "Epoch   3 Batch   90/538 - Train Accuracy: 0.9377, Validation Accuracy: 0.9382, Loss: 0.0569\n",
      "Epoch   3 Batch  100/538 - Train Accuracy: 0.9582, Validation Accuracy: 0.9366, Loss: 0.0409\n",
      "Epoch   3 Batch  110/538 - Train Accuracy: 0.9535, Validation Accuracy: 0.9331, Loss: 0.0403\n",
      "Epoch   3 Batch  120/538 - Train Accuracy: 0.9533, Validation Accuracy: 0.9462, Loss: 0.0326\n",
      "Epoch   3 Batch  130/538 - Train Accuracy: 0.9433, Validation Accuracy: 0.9430, Loss: 0.0431\n",
      "Epoch   3 Batch  140/538 - Train Accuracy: 0.9463, Validation Accuracy: 0.9347, Loss: 0.0616\n",
      "Epoch   3 Batch  150/538 - Train Accuracy: 0.9510, Validation Accuracy: 0.9267, Loss: 0.0468\n",
      "Epoch   3 Batch  160/538 - Train Accuracy: 0.9228, Validation Accuracy: 0.9203, Loss: 0.0458\n",
      "Epoch   3 Batch  170/538 - Train Accuracy: 0.9431, Validation Accuracy: 0.9350, Loss: 0.0463\n",
      "Epoch   3 Batch  180/538 - Train Accuracy: 0.9513, Validation Accuracy: 0.9297, Loss: 0.0499\n",
      "Epoch   3 Batch  190/538 - Train Accuracy: 0.9485, Validation Accuracy: 0.9325, Loss: 0.0615\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Epoch   3 Batch  200/538 - Train Accuracy: 0.9488, Validation Accuracy: 0.9341, Loss: 0.0379\n",
      "Epoch   3 Batch  210/538 - Train Accuracy: 0.9301, Validation Accuracy: 0.9331, Loss: 0.0500\n",
      "Epoch   3 Batch  220/538 - Train Accuracy: 0.9317, Validation Accuracy: 0.9279, Loss: 0.0508\n",
      "Epoch   3 Batch  230/538 - Train Accuracy: 0.9369, Validation Accuracy: 0.9306, Loss: 0.0459\n",
      "Epoch   3 Batch  240/538 - Train Accuracy: 0.9535, Validation Accuracy: 0.9492, Loss: 0.0454\n",
      "Epoch   3 Batch  250/538 - Train Accuracy: 0.9568, Validation Accuracy: 0.9339, Loss: 0.0479\n",
      "Epoch   3 Batch  260/538 - Train Accuracy: 0.9321, Validation Accuracy: 0.9371, Loss: 0.0451\n",
      "Epoch   3 Batch  270/538 - Train Accuracy: 0.9432, Validation Accuracy: 0.9304, Loss: 0.0426\n",
      "Epoch   3 Batch  280/538 - Train Accuracy: 0.9505, Validation Accuracy: 0.9341, Loss: 0.0394\n",
      "Epoch   3 Batch  290/538 - Train Accuracy: 0.9541, Validation Accuracy: 0.9363, Loss: 0.0416\n",
      "Epoch   3 Batch  300/538 - Train Accuracy: 0.9487, Validation Accuracy: 0.9426, Loss: 0.0479\n",
      "Epoch   3 Batch  310/538 - Train Accuracy: 0.9520, Validation Accuracy: 0.9309, Loss: 0.0525\n",
      "Epoch   3 Batch  320/538 - Train Accuracy: 0.9468, Validation Accuracy: 0.9359, Loss: 0.0406\n",
      "Epoch   3 Batch  330/538 - Train Accuracy: 0.9600, Validation Accuracy: 0.9368, Loss: 0.0392\n",
      "Epoch   3 Batch  340/538 - Train Accuracy: 0.9455, Validation Accuracy: 0.9352, Loss: 0.0452\n",
      "Epoch   3 Batch  350/538 - Train Accuracy: 0.9403, Validation Accuracy: 0.9178, Loss: 0.0535\n",
      "Epoch   3 Batch  360/538 - Train Accuracy: 0.9445, Validation Accuracy: 0.9370, Loss: 0.0405\n",
      "Epoch   3 Batch  370/538 - Train Accuracy: 0.9541, Validation Accuracy: 0.9261, Loss: 0.0431\n",
      "Epoch   3 Batch  380/538 - Train Accuracy: 0.9559, Validation Accuracy: 0.9359, Loss: 0.0415\n",
      "Epoch   3 Batch  390/538 - Train Accuracy: 0.9410, Validation Accuracy: 0.9354, Loss: 0.0389\n",
      "Epoch   3 Batch  400/538 - Train Accuracy: 0.9483, Validation Accuracy: 0.9322, Loss: 0.0459\n",
      "Epoch   3 Batch  410/538 - Train Accuracy: 0.9580, Validation Accuracy: 0.9292, Loss: 0.0470\n",
      "Epoch   3 Batch  420/538 - Train Accuracy: 0.9646, Validation Accuracy: 0.9247, Loss: 0.0433\n",
      "Epoch   3 Batch  430/538 - Train Accuracy: 0.9373, Validation Accuracy: 0.9425, Loss: 0.0416\n",
      "Epoch   3 Batch  440/538 - Train Accuracy: 0.9322, Validation Accuracy: 0.9290, Loss: 0.0470\n",
      "Epoch   3 Batch  450/538 - Train Accuracy: 0.9226, Validation Accuracy: 0.9462, Loss: 0.0543\n",
      "Epoch   3 Batch  460/538 - Train Accuracy: 0.9308, Validation Accuracy: 0.9421, Loss: 0.0446\n",
      "Epoch   3 Batch  470/538 - Train Accuracy: 0.9554, Validation Accuracy: 0.9379, Loss: 0.0422\n",
      "Epoch   3 Batch  480/538 - Train Accuracy: 0.9591, Validation Accuracy: 0.9322, Loss: 0.0424\n",
      "Epoch   3 Batch  490/538 - Train Accuracy: 0.9548, Validation Accuracy: 0.9308, Loss: 0.0403\n",
      "Epoch   3 Batch  500/538 - Train Accuracy: 0.9597, Validation Accuracy: 0.9464, Loss: 0.0328\n",
      "Epoch   3 Batch  510/538 - Train Accuracy: 0.9496, Validation Accuracy: 0.9441, Loss: 0.0398\n",
      "Epoch   3 Batch  520/538 - Train Accuracy: 0.9361, Validation Accuracy: 0.9398, Loss: 0.0461\n",
      "Epoch   3 Batch  530/538 - Train Accuracy: 0.9385, Validation Accuracy: 0.9556, Loss: 0.0502\n",
      "Epoch   4 Batch   10/538 - Train Accuracy: 0.9430, Validation Accuracy: 0.9485, Loss: 0.0523\n",
      "Epoch   4 Batch   20/538 - Train Accuracy: 0.9570, Validation Accuracy: 0.9506, Loss: 0.0368\n",
      "Epoch   4 Batch   30/538 - Train Accuracy: 0.9385, Validation Accuracy: 0.9352, Loss: 0.0526\n",
      "Epoch   4 Batch   40/538 - Train Accuracy: 0.9576, Validation Accuracy: 0.9467, Loss: 0.0305\n",
      "Epoch   4 Batch   50/538 - Train Accuracy: 0.9377, Validation Accuracy: 0.9482, Loss: 0.0444\n",
      "Epoch   4 Batch   60/538 - Train Accuracy: 0.9547, Validation Accuracy: 0.9627, Loss: 0.0454\n",
      "Epoch   4 Batch   70/538 - Train Accuracy: 0.9621, Validation Accuracy: 0.9355, Loss: 0.0349\n",
      "Epoch   4 Batch   80/538 - Train Accuracy: 0.9527, Validation Accuracy: 0.9370, Loss: 0.0349\n",
      "Epoch   4 Batch   90/538 - Train Accuracy: 0.9496, Validation Accuracy: 0.9411, Loss: 0.0519\n",
      "Epoch   4 Batch  100/538 - Train Accuracy: 0.9553, Validation Accuracy: 0.9473, Loss: 0.0305\n",
      "Epoch   4 Batch  110/538 - Train Accuracy: 0.9547, Validation Accuracy: 0.9480, Loss: 0.0442\n",
      "Epoch   4 Batch  120/538 - Train Accuracy: 0.9611, Validation Accuracy: 0.9462, Loss: 0.0315\n",
      "Epoch   4 Batch  130/538 - Train Accuracy: 0.9541, Validation Accuracy: 0.9581, Loss: 0.0359\n",
      "Epoch   4 Batch  140/538 - Train Accuracy: 0.9475, Validation Accuracy: 0.9512, Loss: 0.0487\n",
      "Epoch   4 Batch  150/538 - Train Accuracy: 0.9727, Validation Accuracy: 0.9428, Loss: 0.0380\n",
      "Epoch   4 Batch  160/538 - Train Accuracy: 0.9412, Validation Accuracy: 0.9231, Loss: 0.0418\n",
      "Epoch   4 Batch  170/538 - Train Accuracy: 0.9459, Validation Accuracy: 0.9245, Loss: 0.0440\n",
      "Epoch   4 Batch  180/538 - Train Accuracy: 0.9613, Validation Accuracy: 0.9460, Loss: 0.0422\n",
      "Epoch   4 Batch  190/538 - Train Accuracy: 0.9488, Validation Accuracy: 0.9302, Loss: 0.0506\n",
      "Epoch   4 Batch  200/538 - Train Accuracy: 0.9605, Validation Accuracy: 0.9316, Loss: 0.0309\n",
      "Epoch   4 Batch  210/538 - Train Accuracy: 0.9496, Validation Accuracy: 0.9478, Loss: 0.0420\n",
      "Epoch   4 Batch  220/538 - Train Accuracy: 0.9237, Validation Accuracy: 0.9480, Loss: 0.0454\n",
      "Epoch   4 Batch  230/538 - Train Accuracy: 0.9479, Validation Accuracy: 0.9435, Loss: 0.0372\n",
      "Epoch   4 Batch  240/538 - Train Accuracy: 0.9514, Validation Accuracy: 0.9474, Loss: 0.0441\n",
      "Epoch   4 Batch  250/538 - Train Accuracy: 0.9629, Validation Accuracy: 0.9393, Loss: 0.0401\n",
      "Epoch   4 Batch  260/538 - Train Accuracy: 0.9366, Validation Accuracy: 0.9375, Loss: 0.0511\n",
      "Epoch   4 Batch  270/538 - Train Accuracy: 0.9643, Validation Accuracy: 0.9355, Loss: 0.0415\n",
      "Epoch   4 Batch  280/538 - Train Accuracy: 0.9548, Validation Accuracy: 0.9434, Loss: 0.0356\n",
      "Epoch   4 Batch  290/538 - Train Accuracy: 0.9533, Validation Accuracy: 0.9476, Loss: 0.0454\n",
      "Epoch   4 Batch  300/538 - Train Accuracy: 0.9531, Validation Accuracy: 0.9512, Loss: 0.0420\n",
      "Epoch   4 Batch  310/538 - Train Accuracy: 0.9713, Validation Accuracy: 0.9473, Loss: 0.0438\n",
      "Epoch   4 Batch  320/538 - Train Accuracy: 0.9585, Validation Accuracy: 0.9423, Loss: 0.0372\n",
      "Epoch   4 Batch  330/538 - Train Accuracy: 0.9613, Validation Accuracy: 0.9347, Loss: 0.0407\n",
      "Epoch   4 Batch  340/538 - Train Accuracy: 0.9426, Validation Accuracy: 0.9474, Loss: 0.0419\n",
      "Epoch   4 Batch  350/538 - Train Accuracy: 0.9561, Validation Accuracy: 0.9561, Loss: 0.0536\n",
      "Epoch   4 Batch  360/538 - Train Accuracy: 0.9703, Validation Accuracy: 0.9496, Loss: 0.0356\n",
      "Epoch   4 Batch  370/538 - Train Accuracy: 0.9592, Validation Accuracy: 0.9533, Loss: 0.0362\n",
      "Epoch   4 Batch  380/538 - Train Accuracy: 0.9613, Validation Accuracy: 0.9453, Loss: 0.0359\n",
      "Epoch   4 Batch  390/538 - Train Accuracy: 0.9589, Validation Accuracy: 0.9437, Loss: 0.0361\n",
      "Epoch   4 Batch  400/538 - Train Accuracy: 0.9494, Validation Accuracy: 0.9501, Loss: 0.0407\n",
      "Epoch   4 Batch  410/538 - Train Accuracy: 0.9637, Validation Accuracy: 0.9528, Loss: 0.0378\n",
      "Epoch   4 Batch  420/538 - Train Accuracy: 0.9584, Validation Accuracy: 0.9508, Loss: 0.0371\n",
      "Epoch   4 Batch  430/538 - Train Accuracy: 0.9439, Validation Accuracy: 0.9478, Loss: 0.0415\n",
      "Epoch   4 Batch  440/538 - Train Accuracy: 0.9637, Validation Accuracy: 0.9542, Loss: 0.0424\n",
      "Epoch   4 Batch  450/538 - Train Accuracy: 0.9291, Validation Accuracy: 0.9458, Loss: 0.0603\n",
      "Epoch   4 Batch  460/538 - Train Accuracy: 0.9418, Validation Accuracy: 0.9586, Loss: 0.0467\n",
      "Epoch   4 Batch  470/538 - Train Accuracy: 0.9604, Validation Accuracy: 0.9544, Loss: 0.0401\n",
      "Epoch   4 Batch  480/538 - Train Accuracy: 0.9559, Validation Accuracy: 0.9412, Loss: 0.0360\n",
      "Epoch   4 Batch  490/538 - Train Accuracy: 0.9526, Validation Accuracy: 0.9529, Loss: 0.0323\n",
      "Epoch   4 Batch  500/538 - Train Accuracy: 0.9604, Validation Accuracy: 0.9334, Loss: 0.0287\n",
      "Epoch   4 Batch  510/538 - Train Accuracy: 0.9554, Validation Accuracy: 0.9432, Loss: 0.0362\n",
      "Epoch   4 Batch  520/538 - Train Accuracy: 0.9404, Validation Accuracy: 0.9426, Loss: 0.0435\n",
      "Epoch   4 Batch  530/538 - Train Accuracy: 0.9428, Validation Accuracy: 0.9474, Loss: 0.0437\n",
      "Model Trained and Saved\n"
     ]
    }
   ],
   "source": [
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL\n",
    "\"\"\"\n",
    "def get_accuracy(target, logits):\n",
    "    \"\"\"\n",
    "    Calculate accuracy\n",
    "    \"\"\"\n",
    "    max_seq = max(target.shape[1], logits.shape[1])\n",
    "    if max_seq - target.shape[1]:\n",
    "        target = np.pad(\n",
    "            target,\n",
    "            [(0,0),(0,max_seq - target.shape[1])],\n",
    "            'constant')\n",
    "    if max_seq - logits.shape[1]:\n",
    "        logits = np.pad(\n",
    "            logits,\n",
    "            [(0,0),(0,max_seq - logits.shape[1])],\n",
    "            'constant')\n",
    "\n",
    "    return np.mean(np.equal(target, logits))\n",
    "\n",
    "# Split data to training and validation sets\n",
    "train_source = source_int_text[batch_size:]\n",
    "train_target = target_int_text[batch_size:]\n",
    "valid_source = source_int_text[:batch_size]\n",
    "valid_target = target_int_text[:batch_size]\n",
    "(valid_sources_batch, valid_targets_batch, valid_sources_lengths, valid_targets_lengths ) = next(get_batches(valid_source,\n",
    "                                                                                                             valid_target,\n",
    "                                                                                                             batch_size,\n",
    "                                                                                                             source_vocab_to_int['<PAD>'],\n",
    "                                                                                                             target_vocab_to_int['<PAD>']))                                                                                                  \n",
    "with tf.Session(graph=train_graph) as sess:\n",
    "    sess.run(tf.global_variables_initializer())\n",
    "\n",
    "    for epoch_i in range(epochs):\n",
    "        for batch_i, (source_batch, target_batch, sources_lengths, targets_lengths) in enumerate(\n",
    "                get_batches(train_source, train_target, batch_size,\n",
    "                            source_vocab_to_int['<PAD>'],\n",
    "                            target_vocab_to_int['<PAD>'])):\n",
    "\n",
    "            _, loss = sess.run(\n",
    "                [train_op, cost],\n",
    "                {input_data: source_batch,\n",
    "                 targets: target_batch,\n",
    "                 lr: learning_rate,\n",
    "                 target_sequence_length: targets_lengths,\n",
    "                 source_sequence_length: sources_lengths,\n",
    "                 keep_prob: keep_probability})\n",
    "\n",
    "\n",
    "            if batch_i % display_step == 0 and batch_i > 0:\n",
    "\n",
    "\n",
    "                batch_train_logits = sess.run(\n",
    "                    inference_logits,\n",
    "                    {input_data: source_batch,\n",
    "                     source_sequence_length: sources_lengths,\n",
    "                     target_sequence_length: targets_lengths,\n",
    "                     keep_prob: 1.0})\n",
    "\n",
    "\n",
    "                batch_valid_logits = sess.run(\n",
    "                    inference_logits,\n",
    "                    {input_data: valid_sources_batch,\n",
    "                     source_sequence_length: valid_sources_lengths,\n",
    "                     target_sequence_length: valid_targets_lengths,\n",
    "                     keep_prob: 1.0})\n",
    "\n",
    "                train_acc = get_accuracy(target_batch, batch_train_logits)\n",
    "\n",
    "                valid_acc = get_accuracy(valid_targets_batch, batch_valid_logits)\n",
    "\n",
    "                print('Epoch {:>3} Batch {:>4}/{} - Train Accuracy: {:>6.4f}, Validation Accuracy: {:>6.4f}, Loss: {:>6.4f}'\n",
    "                      .format(epoch_i, batch_i, len(source_int_text) // batch_size, train_acc, valid_acc, loss))\n",
    "\n",
    "    # Save Model\n",
    "    saver = tf.train.Saver()\n",
    "    saver.save(sess, save_path)\n",
    "    print('Model Trained and Saved')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Save Parameters\n",
    "Save the `batch_size` and `save_path` parameters for inference."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL\n",
    "\"\"\"\n",
    "# Save parameters for checkpoint\n",
    "helper.save_params(save_path)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Checkpoint"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL\n",
    "\"\"\"\n",
    "import tensorflow as tf\n",
    "import numpy as np\n",
    "import helper\n",
    "import problem_unittests as tests\n",
    "\n",
    "_, (source_vocab_to_int, target_vocab_to_int), (source_int_to_vocab, target_int_to_vocab) = helper.load_preprocess()\n",
    "load_path = helper.load_params()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Sentence to Sequence\n",
    "To feed a sentence into the model for translation, you first need to preprocess it.  Implement the function `sentence_to_seq()` to preprocess new sentences.\n",
    "\n",
    "- Convert the sentence to lowercase\n",
    "- Convert words into ids using `vocab_to_int`\n",
    " - Convert words not in the vocabulary, to the `<UNK>` word id."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Tests Passed\n"
     ]
    }
   ],
   "source": [
    "def sentence_to_seq(sentence, vocab_to_int):\n",
    "    \"\"\"\n",
    "    Convert a sentence to a sequence of ids\n",
    "    :param sentence: String\n",
    "    :param vocab_to_int: Dictionary to go from the words to an id\n",
    "    :return: List of word ids\n",
    "    \"\"\"\n",
    "    # TODO: Implement Function\n",
    "    word_ids = [vocab_to_int.get(word, vocab_to_int.get('<UNK>')) for word in sentence.lower().split()]\n",
    "    return word_ids\n",
    "\n",
    "\n",
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL THAT IS BELOW THIS LINE\n",
    "\"\"\"\n",
    "tests.test_sentence_to_seq(sentence_to_seq)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Translate\n",
    "This will translate `translate_sentence` from English to French."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "INFO:tensorflow:Restoring parameters from checkpoints/dev\n",
      "Input\n",
      "  Word Ids:      [207, 105, 9, 219, 193, 151, 184]\n",
      "  English Words: ['he', 'saw', 'a', 'old', 'yellow', 'truck', '.']\n",
      "\n",
      "Prediction\n",
      "  Word Ids:      [292, 90, 86, 21, 76, 11, 175, 247, 1]\n",
      "  French Words: il a vu un vieux camion jaune . <EOS>\n"
     ]
    }
   ],
   "source": [
    "translate_sentence = 'he saw a old yellow truck .'\n",
    "\n",
    "\n",
    "\"\"\"\n",
    "DON'T MODIFY ANYTHING IN THIS CELL\n",
    "\"\"\"\n",
    "translate_sentence = sentence_to_seq(translate_sentence, source_vocab_to_int)\n",
    "\n",
    "loaded_graph = tf.Graph()\n",
    "with tf.Session(graph=loaded_graph) as sess:\n",
    "    # Load saved model\n",
    "    loader = tf.train.import_meta_graph(load_path + '.meta')\n",
    "    loader.restore(sess, load_path)\n",
    "\n",
    "    input_data = loaded_graph.get_tensor_by_name('input:0')\n",
    "    logits = loaded_graph.get_tensor_by_name('predictions:0')\n",
    "    target_sequence_length = loaded_graph.get_tensor_by_name('target_sequence_length:0')\n",
    "    source_sequence_length = loaded_graph.get_tensor_by_name('source_sequence_length:0')\n",
    "    keep_prob = loaded_graph.get_tensor_by_name('keep_prob:0')\n",
    "\n",
    "    translate_logits = sess.run(logits, {input_data: [translate_sentence]*batch_size,\n",
    "                                         target_sequence_length: [len(translate_sentence)*2]*batch_size,\n",
    "                                         source_sequence_length: [len(translate_sentence)]*batch_size,\n",
    "                                         keep_prob: 1.0})[0]\n",
    "\n",
    "print('Input')\n",
    "print('  Word Ids:      {}'.format([i for i in translate_sentence]))\n",
    "print('  English Words: {}'.format([source_int_to_vocab[i] for i in translate_sentence]))\n",
    "\n",
    "print('\\nPrediction')\n",
    "print('  Word Ids:      {}'.format([i for i in translate_logits]))\n",
    "print('  French Words: {}'.format(\" \".join([target_int_to_vocab[i] for i in translate_logits])))\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Imperfect Translation\n",
    "You might notice that some sentences translate better than others.  Since the dataset you're using only has a vocabulary of 227 English words of the thousands that you use, you're only going to see good results using these words.  For this project, you don't need a perfect translation. However, if you want to create a better translation model, you'll need better data.\n",
    "\n",
    "You can train on the [WMT10 French-English corpus](http://www.statmt.org/wmt10/training-giga-fren.tar).  This dataset has more vocabulary and richer in topics discussed.  However, this will take you days to train, so make sure you've a GPU and the neural network is performing well on dataset we provided.  Just make sure you play with the WMT10 corpus after you've submitted this project.\n",
    "## Submitting This Project\n",
    "When submitting this project, make sure to run all the cells before saving the notebook. Save the notebook file as \"dlnd_language_translation.ipynb\" and save it as a HTML file under \"File\" -> \"Download as\". Include the \"helper.py\" and \"problem_unittests.py\" files in your submission."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "anaconda-cloud": {},
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.5.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}
