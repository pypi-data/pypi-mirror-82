import numpy as np
from astropy.constants import h, c, m_e, sigma_T, G
import astropy.units as u
from .targets import CMB, PointSourceBehindJet, SSDisk, SphericalShellBLR, RingDustTorus


mec2 = m_e.to("erg", equivalencies=u.mass_energy())
# equivalency to transform frequencies to energies in electron rest mass units
epsilon_equivalency = [
    (u.Hz, u.Unit(""), lambda x: h.cgs * x / mec2, lambda x: x * mec2 / h.cgs)
]


__all__ = ["SynchrotronSelfCompton", "ExternalCompton", "cos_psi"]


def F_c(q, gamma_e):
    """isotropic Compton kernel, Eq. 6.75 in [DermerMenon2009]_, Eq. 10 in [Finke2008]_"""
    term_1 = 2 * q * np.log(q)
    term_2 = (1 + 2 * q) * (1 - q)
    term_3 = 1 / 2 * np.power(gamma_e * q, 2) / (1 + gamma_e * q) * (1 - q)
    return term_1 + term_2 + term_3


def isotropic_kernel(gamma, epsilon, epsilon_s):
    """Compton kernel for isotropic nonthermal electrons scattering photons of 
    an isotropic external radiation field.
    Integrand of Eq. 6.74 in [DermerMenon2009]_.

    Parameters
    ----------
    gamma : :class:`~numpy.ndarray`
        Lorentz factors of the electrons distribution
    epsilon : :class:`~numpy.ndarray`
        dimesnionless energies (in electron rest mass units) of the target photons
    epsilon_s : :class:`~numpy.ndarray`
        dimensionless energies (in electron rest mass units) of the scattered photons
    """
    gamma_e = 4 * gamma * epsilon
    q = (epsilon_s / gamma) / (gamma_e * (1 - epsilon_s / gamma))
    q_min = 1 / (4 * np.power(gamma, 2))
    return np.where((q_min <= q) * (q <= 1), F_c(q, gamma_e), 0)


def cos_psi(mu_s, mu, phi):
    """compute the angle between the blob (with zenith mu_s) and a photon with
    zenith and azimuth (mu, phi). The system is symmetric in azimuth for the
    electron phi_s = 0, Eq. 8 in [Finke2016]_."""
    term_1 = mu * mu_s
    term_2 = np.sqrt(1 - np.power(mu, 2)) * np.sqrt(1 - np.power(mu_s, 2))
    term_3 = np.cos(phi)
    return term_1 + term_2 * term_3


def get_gamma_min(epsilon_s, epsilon, mu_s, mu, phi):
    """minimum Lorentz factor for Compton integration, 
    Eq. 29 in [Dermer2009]_, Eq. 38 in [Finke2016]_."""
    sqrt_term = np.sqrt(1 + 2 / (epsilon * epsilon_s * (1 - cos_psi(mu_s, mu, phi))))
    return epsilon_s / 2 * (1 + sqrt_term)


def compton_kernel(gamma, epsilon_s, epsilon, mu_s, mu, phi):
    """angle dependent Compton kernel:
    Eq. 26-27 in [Dermer2009]_.

    Parameters
    ----------
    gamma : :class:`~numpy.ndarray`
        Lorentz factors of the electrons distribution
    epsilon : :class:`~numpy.ndarray`
        dimesnionless energies (in electron rest mass units) of the target photons
    epsilon_s : :class:`~numpy.ndarray`
        dimensionless energies (in electron rest mass units) of the scattered photons
    mu_s : float
        cosine of the zenith angle of the blob w.r.t the jet
    mu : :class:`~numpy.ndarray` or float
        (array of) cosine of the zenith angle subtended by the target
    phi : :class:`~numpy.ndarray` or float
        (array of) of the azimuth angle subtended by the target
    """
    epsilon_bar = gamma * epsilon * (1 - cos_psi(mu_s, mu, phi))
    y = 1 - epsilon_s / gamma
    y_1 = -(2 * epsilon_s) / (gamma * epsilon_bar * y)
    y_2 = np.power(epsilon_s, 2) / np.power(gamma * epsilon_bar * y, 2)
    values = y + 1 / y + y_1 + y_2
    gamma_min = get_gamma_min(epsilon_s, epsilon, mu_s, mu, phi)
    values = np.where(gamma >= gamma_min, y + 1 / y + y_1 + y_2, 0)
    return values


def x_re_shell(mu, R_re, r):
    """distance between the blob and a spherical reprocessing material,
    see Fig. 9 and Eq. 76 in [Finke2016]_.
    
    Parameters
    ----------
    mu : :class:`~numpy.ndarray`
        (array of) cosine of the zenith angle subtended by the target
    R_re : :class:`~astropy.units.Quantity`
        distance from the BH to the reprocessing material
    r : :class:`~astropy.units.Quantity`
        height of the emission region in the jet
    """
    return np.sqrt(np.power(R_re, 2) + np.power(r, 2) - 2 * r * R_re * mu)


def x_re_ring(R_re, r):
    """distance between the blob and a ring reprocessing material"""
    return np.sqrt(np.power(R_re, 2) + np.power(r, 2))


def mu_star(mu, R_re, r):
    """cosine of the angle between the blob and the reprocessing material,
    see Fig. 9 and Eq. 76 in [Finke2016]_.

    Parameters
    ----------
    mu : :class:`~numpy.ndarray`
        (array of) cosine of the zenith angle subtended by the target
    R_re : float 
        distance (in cm) from the BH to the reprocessing material
    r : float
        height (in cm) of the emission region in the jet
    """
    addend = np.power(R_re / x_re_shell(mu, R_re, r), 2) * (1 - np.power(mu, 2))
    return np.sqrt(1 - addend)


class SynchrotronSelfCompton:
    """class for Synchrotron Self Compton radiation computation

    Parameters
    ----------
    blob : :class:`~agnpy.emission_region.Blob`
        emission region and electron distribution hitting the photon target
    synchrotron : :class:`~agnpy.synchrotron.Synchrotron`
        class describing the synchrotron photons target
    """

    def __init__(self, blob, synchrotron):
        self.blob = blob
        self.synchrotron = synchrotron
        # default grid of epsilon values over which for the synchroton emission
        self.epsilon_syn = np.logspace(-13, 10, 300)
        self.synch_sed_emissivity = self.synchrotron.com_sed_emissivity(
            self.epsilon_syn
        )

    def com_sed_emissivity(self, epsilon):
        r"""SSC  emissivity: 

        .. math::
            \epsilon'\,J'_{\mathrm{SSC}}(\epsilon')\,[\mathrm{erg}\,\mathrm{s}^{-1}]
        
        Eq. 8 and 9 of [Finke2008]_.

        **Note:** This emissivity is computed in the co-moving frame of the blob.
        When calling this function from another, these energies
        have to be transformed in the co-moving frame of the plasmoid.

        Parameters
        ----------
        epsilon : :class:`~numpy.ndarray`
            dimensionless energies (in electron rest mass units) of the scattered photons
        """
        gamma = self.blob.gamma
        N_e = self.blob.N_e(gamma).value
        # Eq. 22 of [Finke2008]_, the factor 3 / 4 accounts for averaging in a sphere
        # not included in Dermer and Finke's papers
        J_epsilon_syn = 3 / 4 * self.synch_sed_emissivity / self.epsilon_syn
        # for multidimensional integration
        # axis = 0 : electrons Lorentz factors
        # axis = 1 : target photons energies
        # axis = 2 : scattered photons energies
        # arrays starting with _ are multidimensional and used for integration
        _gamma = np.reshape(gamma, (gamma.size, 1, 1))
        _N_e = np.reshape(N_e, (N_e.size, 1, 1))
        _epsilon_syn = np.reshape(self.epsilon_syn, (1, self.epsilon_syn.size, 1))
        _J_epsilon_syn = np.reshape(J_epsilon_syn, (1, J_epsilon_syn.size, 1))
        _epsilon = np.reshape(epsilon, (1, 1, epsilon.size))
        _kernel = isotropic_kernel(_gamma, _epsilon_syn, _epsilon)
        # build the integrands of Eq. 9 in [2], using the reshaped arrays
        integrand_epsilon = _J_epsilon_syn / np.power(_epsilon_syn, 2)
        integrand_gamma = _N_e / np.power(_gamma, 2) * _kernel
        integrand = integrand_epsilon * integrand_gamma
        # integrate the Lorentz factor and the target synchrotron energies axes
        integral_gamma = np.trapz(integrand, gamma, axis=0)
        integral_epsilon = np.trapz(integral_gamma, self.epsilon_syn, axis=0)
        prefactor = (
            9
            * sigma_T
            * np.power(epsilon, 2)
            / (16 * np.pi * np.power(self.blob.R_b, 2))
        )
        emissivity = prefactor * integral_epsilon
        return emissivity.to("erg s-1")

    def sed_luminosity(self, nu):
        r"""SSC luminosity SED: 

        .. math::
            \nu L_{\nu} \, [\mathrm{erg}\,\mathrm{s}^{-1}]

        Parameters
        ----------
        nu : :class:`~astropy.units.Quantity`
            array of frequencies, in Hz, to compute the sed, **note** these are 
            observed frequencies (observer frame).
        """
        epsilon = nu.to("", equivalencies=epsilon_equivalency)
        # correct epsilon to the jet comoving frame
        epsilon_prime = (1 + self.blob.z) * epsilon / self.blob.delta_D
        prefactor = np.power(self.blob.delta_D, 4)
        return prefactor * self.com_sed_emissivity(epsilon_prime)

    def sed_flux(self, nu):
        r"""SSC flux SED:
        
        .. math::
            \nu F_{\nu} \, [\mathrm{erg}\,\mathrm{cm}^{-2}\,\mathrm{s}^{-1}]
        
        Eq. 15 in [Finke2008]_

        Parameters
        ----------
        nu : :class:`~astropy.units.Quantity`
            array of frequencies, in Hz, to compute the sed, **note** these are 
            observed frequencies (observer frame).
        """
        epsilon = nu.to("", equivalencies=epsilon_equivalency)
        # correct epsilon to the jet comoving frame
        epsilon_prime = (1 + self.blob.z) * epsilon / self.blob.delta_D
        prefactor = np.power(self.blob.delta_D, 4) / (
            4 * np.pi * np.power(self.blob.d_L, 2)
        )
        sed = prefactor * self.com_sed_emissivity(epsilon_prime)
        return sed.to("erg cm-2 s-1")

    def sed_peak_flux(self, nu):
        """provided a grid of frequencies nu, returns the peak flux of the SED
        """
        return self.sed_flux(nu).max()

    def sed_peak_nu(self, nu):
        """provided a grid of frequencies nu, returns the frequency at which the SED peaks
        """
        idx_max = self.sed_flux(nu).argmax()
        return nu[idx_max]


class ExternalCompton:
    """class for External Compton radiation computation

    Parameters
    ----------
    blob : :class:`~agnpy.emission_region.Blob`
        emission region and electron distribution hitting the photon target
    target : :class:`~agnpy.targets`
        class describing the target photon field    
    r : `~astropy.units.Quantity`
        distance of the blob from the Black Hole (i.e. from the target photons)
    """

    def __init__(self, blob, target, r=None):
        self.blob = blob
        # we integrate on a larger grid to account for the transformation
        # of the electron density in the reference frame of the BH
        self.gamma = self.blob.gamma_to_integrate
        # N_e in the reference frame of the galaxy
        self.transformed_N_e = self.blob.N_e(self.gamma / self.blob.delta_D).value
        self.target = target
        self.r = r
        self.set_mu()
        self.set_phi()

    def set_mu(self, mu_size=100):
        self.mu_size = mu_size
        if isinstance(self.target, SSDisk):
            # in case of hte disk the mu interval does not go from -1 to 1
            r_tilde = (self.r / self.target.R_g).to_value("")
            self.mu = self.target.mu_from_r_tilde(r_tilde)
        else:
            self.mu = np.linspace(-1, 1, self.mu_size)

    def set_phi(self, phi_size=50):
        self.phi_size = phi_size
        self.phi = np.linspace(0, 2 * np.pi, self.phi_size)

    def _sed_flux_cmb(self, nu):
        """SED flux for EC on CMB
        
        Parameters
        ----------
        nu : `~astropy.units.Quantity`
            array of frequencies, in Hz, to compute the sed, **note** these are 
            observed frequencies (observer frame).
        """
        # define the dimensionless energy
        epsilon_s = nu.to("", equivalencies=epsilon_equivalency)
        # transform to BH frame
        epsilon_s *= 1 + self.blob.z
        # for multidimensional integration
        # axis 0: gamma
        # axis 1: mu
        # axis 2: phi
        # axis 3: epsilon_s
        # arrays starting with _ are multidimensional and used for integration
        _gamma = np.reshape(self.gamma, (self.gamma.size, 1, 1, 1))
        _N_e = np.reshape(self.transformed_N_e, (self.transformed_N_e.size, 1, 1, 1))
        _mu = np.reshape(self.mu, (1, self.mu.size, 1, 1))
        _phi = np.reshape(self.phi, (1, 1, self.phi.size, 1))
        _epsilon_s = np.reshape(epsilon_s, (1, 1, 1, epsilon_s.size))
        # define integrating function
        _kernel = compton_kernel(
            _gamma, _epsilon_s, self.target.epsilon_0, self.blob.mu_s, _mu, _phi
        )
        _integrand = np.power(_gamma, -2) * _N_e * _kernel
        integral_gamma = np.trapz(_integrand, self.gamma, axis=0)
        integral_mu = np.trapz(integral_gamma, self.mu, axis=0)
        integral_phi = np.trapz(integral_mu, self.phi, axis=0)
        prefactor_num = (
            3
            * c
            * sigma_T
            * self.target.u_0
            * np.power(epsilon_s, 2)
            * np.power(self.blob.delta_D, 3)
        )
        prefactor_denom = (
            np.power(2, 7)
            * np.power(np.pi, 2)
            * np.power(self.blob.d_L, 2)
            * np.power(self.target.epsilon_0, 2)
        )
        sed = prefactor_num / prefactor_denom * integral_phi
        return sed.to("erg cm-2 s-1")

    def _sed_flux_point_source(self, nu):
        """SED flux for EC on a point like source behind the jet
        
        Parameters
        ----------
        nu : `~astropy.units.Quantity`
            array of frequencies, in Hz, to compute the sed, **note** these are 
            observed frequencies (observer frame).
        """
        # define the dimensionless energy
        epsilon_s = nu.to("", equivalencies=epsilon_equivalency)
        # transform to BH frame
        epsilon_s *= 1 + self.blob.z
        # for multidimensional integration
        # axis 0: gamma
        # axis 1: epsilon_s
        # arrays starting with _ are multidimensional and used for integration
        _gamma = np.reshape(self.gamma, (self.gamma.size, 1))
        _N_e = np.reshape(self.transformed_N_e, (self.transformed_N_e.size, 1))
        _epsilon_s = np.reshape(epsilon_s, (1, epsilon_s.size))
        # define integrating function
        # notice once the value of mu = 1, phi can assume any value, we put 0
        # convenience
        _kernel = compton_kernel(
            _gamma, _epsilon_s, self.target.epsilon_0, self.blob.mu_s, 1, 0
        )
        _integrand = np.power(_gamma, -2) * _N_e * _kernel
        integral_gamma = np.trapz(_integrand, self.gamma, axis=0)
        prefactor_num = (
            3
            * sigma_T
            * self.target.L_0
            * np.power(epsilon_s, 2)
            * np.power(self.blob.delta_D, 3)
        )
        prefactor_denom = (
            np.power(2, 7)
            * np.power(np.pi, 2)
            * np.power(self.blob.d_L, 2)
            * np.power(self.r, 2)
            * np.power(self.target.epsilon_0, 2)
        )
        sed = prefactor_num / prefactor_denom * integral_gamma
        return sed.to("erg cm-2 s-1")

    def _sed_flux_disk(self, nu):
        """SED flux for EC on SS Disk

        Parameters
        ----------
        nu : `~astropy.units.Quantity`
            array of frequencies, in Hz, to compute the sed, **note** these are 
            observed frequencies (observer frame).
        """
        # define the dimensionless energy
        epsilon_s = nu.to("", equivalencies=epsilon_equivalency)
        # transform to BH frame
        epsilon_s *= 1 + self.blob.z
        # for multidimensional integration
        # axis 0: gamma
        # axis 1: mu
        # axis 2: phi
        # axis 3: epsilon_s
        # arrays starting with _ are multidimensional and used for integration
        # distance from the disk in gravitational radius units
        r_tilde = (self.r / self.target.R_g).to_value("")
        _gamma = np.reshape(self.gamma, (self.gamma.size, 1, 1, 1))
        _N_e = np.reshape(self.transformed_N_e, (self.transformed_N_e.size, 1, 1, 1))
        _mu = np.reshape(self.mu, (1, self.mu.size, 1, 1))
        _phi = np.reshape(self.phi, (1, 1, self.phi.size, 1))
        _epsilon_s = np.reshape(epsilon_s, (1, 1, 1, epsilon_s.size))
        _epsilon = self.target.epsilon_mu(_mu, r_tilde)
        # define integrating function
        _kernel = compton_kernel(
            _gamma, _epsilon_s, _epsilon, self.blob.mu_s, _mu, _phi
        )
        _integrand_mu_num = self.target.phi_disk_mu(_mu, r_tilde)
        _integrand_mu_denum = (
            np.power(_epsilon, 2) * _mu * np.power(np.power(_mu, -2) - 1, 3 / 2)
        )
        _integrand = (
            _integrand_mu_num
            / _integrand_mu_denum
            * np.power(_gamma, -2)
            * _N_e
            * _kernel
        )
        integral_gamma = np.trapz(_integrand, self.gamma, axis=0)
        integral_mu = np.trapz(integral_gamma, self.mu, axis=0)
        integral_phi = np.trapz(integral_mu, self.phi, axis=0)
        prefactor_num = (
            9
            * sigma_T
            * G
            * self.target.M_BH
            * self.target.m_dot
            * np.power(epsilon_s, 2)
            * np.power(self.blob.delta_D, 3)
        )
        prefactor_denom = (
            np.power(2, 9)
            * np.power(np.pi, 3)
            * np.power(self.blob.d_L, 2)
            * np.power(self.r, 3)
        )
        sed = prefactor_num / prefactor_denom * integral_phi
        return sed.to("erg cm-2 s-1")

    def _sed_flux_shell_blr(self, nu):
        """SED flux for EC on BLR

        Parameters
        ----------
        nu : `~astropy.units.Quantity`
            array of frequencies, in Hz, to compute the sed, **note** these are 
            observed frequencies (observer frame).
        """
        # define the dimensionless energy
        epsilon_s = nu.to("", equivalencies=epsilon_equivalency)
        # transform to BH frame
        epsilon_s *= 1 + self.blob.z
        # for multidimensional integration
        # axis 0: gamma
        # axis 1: mu_re (cosine zenith from BH to re-processing material)
        # axis 2: phi
        # axis 3: epsilon_s
        # arrays starting with _ are multidimensional and used for integration
        _gamma = np.reshape(self.gamma, (self.gamma.size, 1, 1, 1))
        _N_e = np.reshape(self.transformed_N_e, (self.transformed_N_e.size, 1, 1, 1))
        _mu = np.reshape(self.mu, (1, self.mu.size, 1, 1))
        _phi = np.reshape(self.phi, (1, 1, self.phi.size, 1))
        _epsilon_s = np.reshape(epsilon_s, (1, 1, 1, epsilon_s.size))
        # define integrating functionlue
        _x = x_re_shell(_mu, self.target.R_line, self.r)
        _mu_star = mu_star(_mu, self.target.R_line, self.r)
        _kernel = compton_kernel(
            _gamma, _epsilon_s, self.target.epsilon_line, self.blob.mu_s, _mu_star, _phi
        )
        _integrand = np.power(_x, -2) * np.power(_gamma, -2) * _N_e * _kernel
        integral_gamma = np.trapz(_integrand, self.gamma, axis=0)
        integral_mu = np.trapz(integral_gamma, self.mu, axis=0)
        integral_phi = np.trapz(integral_mu, self.phi, axis=0)
        prefactor_num = (
            3
            * sigma_T
            * self.target.xi_line
            * self.target.L_disk
            * np.power(epsilon_s, 2)
            * np.power(self.blob.delta_D, 3)
        )
        prefactor_denom = (
            np.power(2, 9)
            * np.power(np.pi, 3)
            * np.power(self.blob.d_L, 2)
            * np.power(self.target.epsilon_line, 2)
        )
        sed = prefactor_num / prefactor_denom * integral_phi
        return sed.to("erg cm-2 s-1")

    def _sed_flux_ring_torus(self, nu):
        """SED flux for EC on DT

        Parameters
        ----------
        nu : `~astropy.units.Quantity`
            array of frequencies, in Hz, to compute the sed, **note** these are 
            observed frequencies (observer frame).
        """
        # define the dimensionless energy
        epsilon_s = nu.to("", equivalencies=epsilon_equivalency)
        # transform to BH frame
        epsilon_s *= 1 + self.blob.z
        # for multidimensional integration
        # axis 0: gamma
        # axis 1: phi
        # axis 2: epsilon_s
        # arrays starting with _ are multidimensional and used for integration
        x_re = x_re_ring(self.target.R_dt, self.r)
        # here we plug mu =  r / x. Delta function in Eq. 91 of [Finke2016]_
        mu = (self.r / x_re).to_value("")
        _gamma = np.reshape(self.gamma, (self.gamma.size, 1, 1))
        _N_e = np.reshape(self.transformed_N_e, (self.transformed_N_e.size, 1, 1))
        _phi = np.reshape(self.phi, (1, self.phi.size, 1))
        _epsilon_s = np.reshape(epsilon_s, (1, 1, epsilon_s.size))
        # define integrating function
        _kernel = compton_kernel(
            _gamma, _epsilon_s, self.target.epsilon_dt, self.blob.mu_s, mu, _phi
        )
        _integrand = np.power(_gamma, -2) * _N_e * _kernel
        integral_gamma = np.trapz(_integrand, self.gamma, axis=0)
        integral_phi = np.trapz(integral_gamma, self.phi, axis=0)
        prefactor_num = (
            3
            * sigma_T
            * self.target.xi_dt
            * self.target.L_disk
            * np.power(epsilon_s, 2)
            * np.power(self.blob.delta_D, 3)
        )
        prefactor_denom = (
            np.power(2, 8)
            * np.power(np.pi, 3)
            * np.power(self.blob.d_L, 2)
            * np.power(x_re, 2)
            * np.power(self.target.epsilon_dt, 2)
        )
        sed = prefactor_num / prefactor_denom * integral_phi
        return sed.to("erg cm-2 s-1")

    def sed_flux(self, nu):
        """flux SED for EC

        Parameters
        ----------
        nu : `~astropy.units.Quantity`
            array of frequencies, in Hz, to compute the sed, **note** these are 
            observed frequencies (observer frame).
        """
        if isinstance(self.target, CMB):
            return self._sed_flux_cmb(nu)
        if isinstance(self.target, PointSourceBehindJet):
            return self._sed_flux_point_source(nu)
        if isinstance(self.target, SSDisk):
            return self._sed_flux_disk(nu)
        if isinstance(self.target, SphericalShellBLR):
            return self._sed_flux_shell_blr(nu)
        if isinstance(self.target, RingDustTorus):
            return self._sed_flux_ring_torus(nu)

    def sed_peak_flux(self, nu):
        """provided a grid of frequencies nu, returns the peak flux of the SED
        """
        return self.sed_flux(nu).max()

    def sed_peak_nu(self, nu):
        """provided a grid of frequencies nu, returns the frequency at which the SED peaks
        """
        idx_max = self.sed_flux(nu).argmax()
        return nu[idx_max]
