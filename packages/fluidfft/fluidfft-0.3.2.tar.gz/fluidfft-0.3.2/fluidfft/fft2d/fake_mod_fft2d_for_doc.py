class FFT2dFakeForDoc(object):
    """Perform Fast Fourier Transform in 2d.

    Parameters
    ----------

    n0 : int

      Global size over the first dimension in spatial space. This corresponds
      to the y direction.

    n1 : int

      Global size over the second dimension in spatial space. This corresponds
      to the x direction.

    """

    def __init__(self, n0=2, n1=2):
        pass

    def _numpy_api(self):
        """A ``@property`` which imports and returns a NumPy-like array backend."""

    def get_short_name(self):
        """Produce a short name of this object."""

    def get_local_size_X(self):
        """Get the local size in the real space."""

    def run_tests(self):
        """Run the c++ tests."""

    def run_benchs(self, nb_time_execute=10):
        """Run the c++ benchmarcks"""

    def fft_as_arg(self, fieldX, fieldK):
        """Perform the fft and copy the result in the second argument."""

    def ifft_as_arg(self, fieldK, fieldX):
        """Perform the ifft and copy the result in the second argument."""

    def fft(self, fieldX):
        """Perform the fft and returns the result."""

    def ifft(self, fieldK):
        """Perform the ifft and returns the result."""

    def get_shapeX_loc(self):
        """Get the local shape of the array in the "real space"."""

    def get_shapeK_loc(self):
        """Get the local shape of the array in the Fourier space"""

    def get_shapeX_seq(self):
        """Get the shape of the real array as it would be with nb_proc = 1"""

    def get_shapeK_seq(self):
        """Get the shape of the complex array as it would be with nb_proc = 1

        Warning: if get_is_transposed(), the complex array would also be
        transposed, so in this case, one should write::

          nKy = self.get_shapeK_seq[1]

        """

    def get_is_transposed(self):
        """Get the boolean "is_transposed"."""

    def get_seq_indices_first_X(self):
        """Get the "sequential" index of the first number in real space."""

    def get_seq_indices_first_K(self):
        """Get the "sequential" index of the first number in Fourier space."""

    def get_k_adim_loc(self):
        """Get the non-dimensional wavenumbers stored locally.

        Returns
        -------

        k0_adim_loc : np.ndarray

        k1_adim_loc : np.ndarray

        The indices correspond to the index of the dimension in spectral space.
        """

    def get_x_adim_loc(self):
        """Get the coordinates of the points stored locally.

        Returns
        -------

        x0loc : np.ndarray

        x1loc : np.ndarray

        The indices correspond to the index of the dimension in real space.
        """

    def compute_energy_from_X(self, fieldX):
        """Compute the mean energy from a real space array."""

    def compute_energy_from_K(self, fieldK):
        """Compute the mean energy from a Fourier space array."""

    def sum_wavenumbers(self, fieldK):
        """Compute the sum over all wavenumbers."""

    def gather_Xspace(self, ff_loc, root=None):
        """Gather an array in real space for a parallel run."""

    def scatter_Xspace(self, ff_seq, root=None):
        """Scatter an array in real space for a parallel run."""

    def create_arrayX(self, value=None, shape=None):
        """Return a constant array in real space."""

    def create_arrayK(self, value=None, shape=None):
        """Return a constant array in real space."""
