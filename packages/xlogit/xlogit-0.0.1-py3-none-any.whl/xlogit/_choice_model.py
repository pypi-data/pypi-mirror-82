"""
Implements multinomial and mixed logit models
"""
# pylint: disable=invalid-name

import numpy as np
from scipy.stats import t
from abc import ABC, abstractmethod


class ChoiceModel(ABC):
    """Base class for estimation of discrete choice models"""

    def __init__(self):
        """Init Function

        Parameters
        ----------
        random_state: an integer used as seed to generate numpy random numbers
        """
        self.coeff_names = None
        self.coeff_ = None
        self.stderr = None
        self.zvalues = None
        self.pvalues = None
        self.loglikelihood = None

    def _reset_attributes(self):
        self.coeff_names = None
        self.coeff_ = None
        self.stderr = None
        self.zvalues = None
        self.pvalues = None
        self.loglikelihood = None

    @abstractmethod
    def fit(self, X, y, varnames=None, alt=None, isvars=None,
            base_alt=None, fit_intercept=False, init_coeff=None, maxiter=2000,
            random_state=None):
        pass

    def _pre_fit(self, alt, varnames, isvars, base_alt,
                 fit_intercept, maxiter):
        self._reset_attributes()
        self.isvars = [] if not isvars else isvars
        self.asvars = list(set(varnames) - set(self.isvars))
        self.varnames = varnames
        self.fit_intercept = fit_intercept
        self.alt = alt
        self.base_alt = alt[0] if base_alt is None else base_alt
        self.maxiter = maxiter

    def _post_fit(self, optimization_res, coeff_names, N, verbose=1):
        self.convergence = optimization_res['success']
        self.coeff_ = optimization_res['x']
        self.stderr = np.sqrt(np.diag(optimization_res['hess_inv']))
        self.zvalues = self.coeff_/self.stderr
        self.pvalues = 2*t.pdf(-np.abs(self.zvalues), df=N)  # two tailed test
        self.loglikelihood = -optimization_res['fun']
        self.coeff_names = coeff_names
        self.total_iter = optimization_res['nit']
        if self.convergence and verbose > 0:
            print("Estimation succesfully completed after {} iterations. "
                  "Use .summary() to see the estimated values"
                  .format(self.total_iter))
        if not self.convergence and verbose > 0:
            print("**** The optimization did not converge after {} "
                  "iterations. ****".format(self.total_iter))
            print("Message: "+optimization_res['message'])

    def _setup_design_matrix(self, X):
        J = len(self.alt)
        N = int(len(X)/J)
        isvars = self.isvars.copy()
        asvars = self.asvars.copy()
        varnames = self.varnames.copy()

        if self.fit_intercept:
            isvars.insert(0, '_intercept')
            varnames.insert(0, '_intercept')
            X = np.hstack((np.ones(J*N)[:, None], X))

        ispos = [varnames.index(i) for i in isvars]  # Position of IS vars
        aspos = [varnames.index(i) for i in asvars]  # Position of AS vars

        # Create design matrix
        # For individual specific variables
        if isvars:
            # Create a dummy individual specific variables for the alt
            dummy = np.tile(np.eye(J), reps=(N, 1))
            # Remove base alternative
            dummy = np.delete(dummy,
                              self.alt.index(self.base_alt), axis=1)
            Xis = X[:, ispos]
            # Multiply dummy representation by the individual specific data
            Xis = np.einsum('ij,ik->ijk', Xis, dummy)
            Xis = Xis.reshape(N, J, (J-1)*len(ispos))

        # For alternative specific variables
        if asvars:
            Xas = X[:, aspos]
            Xas = Xas.reshape(N, J, -1)

        # Set design matrix based on existance of asvars and isvars
        if asvars and isvars:
            X = np.dstack((Xis, Xas))
        elif asvars:
            X = Xas
        elif isvars:
            X = Xis

        names = ["{}.{}".format(isvar, j) for isvar in isvars
                 for j in self.alt if j != self.base_alt] + asvars
        names = np.array(names)

        return X, names

    def _validate_inputs(self, X, y, alt, varnames, isvars, base_alt,
                         fit_intercept, max_iterations):
        if not varnames:
            raise ValueError('The parameter varnames is required')
        if not alt:
            raise ValueError('The parameter alternatives is required')
        if X.ndim != 2:
            raise ValueError("X must be an array of two dimensions in "
                             "long format")
        if y.ndim != 1:
            raise ValueError("y must be an array of one dimension in "
                             "long format")
        if len(varnames) != X.shape[1]:
            raise ValueError("The length of varnames must match the number "
                             "of columns in X")

    def summary(self):
        """
        Prints in console the coefficients and additional estimation outputs
        """
        if self.coeff_ is None:
            print("The current model has not been yet estimated")
            return
        if not self.convergence:
            print("-"*50)
            print("WARNING: Convergence was not reached during estimation. "
                  "The given estimates may not be reliable")
            print('*'*50)
        print("-"*75)
        print("{:19} {:>13} {:>13} {:>13} {:>13}"
              .format("Coefficient", "Estimate", "Std.Err.", "z-val", "P>|z|"))
        print("-"*75)
        fmt = "{:19} {:13.7f} {:13.7f} {:13.7f} {:13.3g} {:3}"
        for i in range(len(self.coeff_)):
            signif = ""
            if self.pvalues[i] < 0.001:
                signif = "***"
            elif self.pvalues[i] < 0.01:
                signif = "**"
            elif self.pvalues[i] < 0.05:
                signif = "*"
            elif self.pvalues[i] < 0.1:
                signif = "."
            print(fmt.format(self.coeff_names[i][:19], self.coeff_[i],
                             self.stderr[i], self.zvalues[i], self.pvalues[i],
                             signif))
        print("-"*75)
        print("Significance:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1")
        print("")
        print("Log-Likelihood= {:.3f}".format(self.loglikelihood))
