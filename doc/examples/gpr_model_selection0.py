#!/usr/bin/env python
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   Copyright (c) 2008 Emanuele Olivetti <emanuele@relativita.com>
#   See COPYING file distributed along with the PyMVPA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""
Run simple model selection (grid search over hyperparameters' space) of
Gaussian Process Regression (GPR) on a simple 1D example.
"""

__docformat__ = 'restructuredtext'

import numpy as N
from mvpa.suite import *
import pylab as P

# Generate train and test dataset:
train_size = 40
test_size = 100
F = 1
dataset = data_generators.sinModulated(train_size, F)
dataset_test = data_generators.sinModulated(test_size, F, flat=True)

print "Looking for better hyperparameters: grid search"

# definition of the search grid:
sigma_noise_steps = N.linspace(0.1, 0.5, num=20)
length_scale_steps = N.linspace(0.05, 0.6, num=20)

# Evaluation of log maringal likelohood spanning the hyperparameters' grid:
lml = N.zeros((len(sigma_noise_steps), len(length_scale_steps)))
lml_best = -N.inf
length_scale_best = 0.0
sigma_noise_best = 0.0
i = 0
for x in sigma_noise_steps:
    j = 0
    for y in length_scale_steps:
        kse = SquaredExponentialKernel(length_scale=y)
        g = GPR(kse, sigma_noise=x, regression=True)
        g.states.enable("log_marginal_likelihood")
        g.train(dataset)
        lml[i, j] = g.states.log_marginal_likelihood
        if lml[i, j] > lml_best:
            lml_best = lml[i, j]
            length_scale_best = y
            sigma_noise_best = x
            # print x,y,lml_best
            pass
        j += 1
        pass
    i += 1
    pass

# Log marginal likelihood contour plot:
P.figure()
X = N.repeat(sigma_noise_steps[:, N.newaxis], sigma_noise_steps.size,
             axis=1)
Y = N.repeat(length_scale_steps[N.newaxis, :], length_scale_steps.size,
             axis=0)
step = (lml.max()-lml.min())/30
P.contour(X, Y, lml, N.arange(lml.min(), lml.max()+step, step),
              colors='k')
P.plot([sigma_noise_best], [length_scale_best], "k+",
           markeredgewidth=2, markersize=8)
P.xlabel("noise standard deviation")
P.ylabel("characteristic length_scale")
P.title("log marginal likelihood")
P.axis("tight")
print "lml_best", lml_best
print "sigma_noise_best", sigma_noise_best
print "length_scale_best", length_scale_best
print "number of expected upcrossing on the unitary intervale:", \
      1.0/(2*N.pi*length_scale_best)


# TODO: reincarnate by providing a function within gpr.py
#
# Plot predicted values using best hyperparameters:
# P.figure()
# compute_prediction(1.0, length_scale_best, sigma_noise_best, True, dataset,
#                    dataset_test.samples, dataset_test.labels, F, True)
if cfg.getboolean('examples', 'interactive', True):
    # show all the cool figures
    P.show()
