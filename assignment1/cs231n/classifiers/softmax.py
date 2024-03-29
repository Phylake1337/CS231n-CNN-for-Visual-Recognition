import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_classes = W.shape[1]
  num_train = X.shape[0]

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  for i in range(num_train):
      score = np.dot(X[i],W)
      eScore = np.exp(score)
      loss += -np.log(eScore[y[i]]/np.sum(eScore))
  
      dW[:, y[i]] += (-1) * (np.sum(eScore) - eScore[y[i]]) / np.sum(eScore) * X[i]
      for j in range(num_classes):
          # pass correct class gradient
          if j == y[i]:
              continue
          # for incorrect classes
          dW[:, j] += np.exp(score[j]) / np.sum(eScore) * X[i]
          
          
  loss /= num_train    
  loss += .5*reg*np.sum(W*W)
  dW /= num_train
  dW += 2 * reg * W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  # loss
  # score: N by C matrix containing class scores
  scores = X.dot(W)
  scores -= scores.max()
  scores = np.exp(scores)
  scores_sums = np.sum(scores, axis=1)
  cors = scores[range(num_train), y]
  loss = cors / scores_sums
  loss = -np.sum(np.log(loss))/num_train + reg * np.sum(W * W)

  # grad
  s = np.divide(scores, scores_sums.reshape(num_train, 1))
  s[range(num_train), y] = - (scores_sums - cors) / scores_sums
  dW = X.T.dot(s)
  dW /= num_train
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

