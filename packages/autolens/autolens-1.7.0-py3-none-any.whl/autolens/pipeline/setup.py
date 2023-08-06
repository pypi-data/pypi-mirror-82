import autofit as af
from autoconf import conf
from autogalaxy.pipeline import setup
from autoarray.inversion import pixelizations as pix, regularization as reg
from autogalaxy.profiles import mass_profiles as mp, light_and_mass_profiles as lmp
from autolens import exc


class SetupHyper(setup.SetupHyper):
    def __init__(
        self,
        hyper_galaxies_lens: bool = False,
        hyper_galaxies_source: bool = False,
        hyper_image_sky: bool = False,
        hyper_background_noise: bool = False,
        hyper_galaxy_phase_first: bool = False,
        hyper_fixed_after_source=False,
        hyper_galaxies_search: af.NonLinearSearch = None,
        inversion_search: af.NonLinearSearch = None,
        hyper_combined_search: af.NonLinearSearch = None,
        evidence_tolerance: float = None,
    ):

        if hyper_galaxies_lens or hyper_galaxies_source:
            hyper_galaxies = True
        else:
            hyper_galaxies = False

        super().__init__(
            hyper_galaxies=hyper_galaxies,
            hyper_image_sky=hyper_image_sky,
            hyper_background_noise=hyper_background_noise,
            hyper_galaxy_phase_first=hyper_galaxy_phase_first,
            hyper_fixed_after_source=hyper_fixed_after_source,
            hyper_galaxies_search=hyper_galaxies_search,
            inversion_search=inversion_search,
            hyper_combined_search=hyper_combined_search,
            evidence_tolerance=evidence_tolerance,
        )

        self.hyper_galaxies_lens = hyper_galaxies_lens
        self.hyper_galaxies_source = hyper_galaxies_source

        if self.hyper_galaxies_lens or self.hyper_galaxies_source:
            self.hyper_galaxy_names = []

        if self.hyper_galaxies_lens:
            self.hyper_galaxy_names.append("lens")

        if self.hyper_galaxies_source:
            self.hyper_galaxy_names.append("source")

    @property
    def hyper_galaxies_tag(self):
        """Tag if hyper-galaxies are used in a hyper pipeline to customize pipeline output paths.

        This is used to generate an overall hyper tag in *hyper_tag*.
        """
        if not self.hyper_galaxies:
            return ""

        hyper_galaxies_tag = conf.instance.setup_tag.get("hyper", "hyper_galaxies")

        if self.hyper_galaxies_lens:
            hyper_galaxies_lens_tag = (
                f"_{conf.instance.setup_tag.get('hyper', 'hyper_galaxies_lens')}"
            )
        else:
            hyper_galaxies_lens_tag = ""

        if self.hyper_galaxies_source:
            hyper_galaxies_source_tag = (
                f"_{conf.instance.setup_tag.get('hyper', 'hyper_galaxies_source')}"
            )
        else:
            hyper_galaxies_source_tag = ""

        return (
            f"{hyper_galaxies_tag}{hyper_galaxies_lens_tag}{hyper_galaxies_source_tag}"
        )


class SetupLightParametric(setup.SetupLightParametric):
    def __init__(
        self,
        light_centre: (float, float) = None,
        align_bulge_disk_centre: bool = False,
        align_bulge_disk_elliptical_comps: bool = False,
        disk_as_sersic: bool = False,
        include_envelope: bool = False,
        envelope_as_sersic: bool = False,
    ):
        """The setup of the light modeling in a pipeline, which controls how PyAutoGalaxy template pipelines runs, for
        example controlling assumptions about the bulge-disk model.

        Users can write their own pipelines which do not use or require the *SetupLightParametric* class.

        This class enables pipeline tagging, whereby the setup of the pipeline is used in the template pipeline
        scripts to tag the output path of the results depending on the setup parameters. This allows one to fit
        different models to a dataset in a structured path format.

        Parameters
        ----------
        light_centre : (float, float) or None
           If input, a fixed (y,x) centre of the galaxy is used for the lens light profile model which is not treated
           as a free parameter by the non-linear search.
        align_bulge_disk_centre : bool
            If a bulge + disk light model (e.g. EllipticalSersic + EllipticalExponential) is used to fit the galaxy,
            `True` will align the centre of the bulge and disk components and not fit them separately.
        align_bulge_disk_elliptical_comps : bool
            If a bulge + disk light model (e.g. EllipticalSersic + EllipticalExponential) is used to fit the galaxy,
            `True` will align the elliptical components the bulge and disk components and not fit them separately.
        disk_as_sersic : bool
            If a bulge + disk light model (e.g. EllipticalSersic + EllipticalExponential) is used to fit the galaxy,
            `True` will use an EllipticalSersic for the disk instead of an EllipticalExponential.
        """

        super().__init__(
            light_centre=light_centre,
            align_bulge_disk_centre=align_bulge_disk_centre,
            align_bulge_disk_elliptical_comps=align_bulge_disk_elliptical_comps,
            disk_as_sersic=disk_as_sersic,
            include_envelope=include_envelope,
            envelope_as_sersic=envelope_as_sersic,
        )


class SetupMassTotal(setup.SetupMassTotal):
    def __init__(
        self,
        mass_prior_model: mp.MassProfile = None,
        with_shear=True,
        mass_centre: (float, float) = None,
    ):
        """The setup of mass modeling in a pipeline, which controls how PyAutoLens template pipelines runs, for
        example controlling assumptions about the mass-to-light profile used too control how a light profile is
        converted to a mass profile.

        Users can write their own pipelines which do not use or require the *SetupPipeline* class.

        This class enables pipeline tagging, whereby the setup of the pipeline is used in the template pipeline
        scripts to tag the output path of the results depending on the setup parameters. This allows one to fit
        different models to a dataset in a structured path format.

        Parameters
        ----------
        mass_centre : (float, float)
           If input, a fixed (y,x) centre of the mass profile is used which is not treated as a free parameter by the
           non-linear search.
        """

        super().__init__(mass_prior_model=mass_prior_model, mass_centre=mass_centre)

        self.with_shear = with_shear

    @property
    def with_shear_tag(self):
        """Generate a tag if an `ExternalShear` is included in the mass model of the pipeline  are
        fixedto a previous estimate, or varied during the analysis, to customize pipeline output paths..

        For the the default configuration files `config/notation/setup_tags.ini` tagging is performed as follows:

        with_shear = `False` -> setup__with_shear
        with_shear = `True` -> setup___with_shear
        """
        if not self.with_shear:
            return "__" + conf.instance.setup_tag.get("mass", "with_shear")
        return "__" + conf.instance.setup_tag.get("mass", "with_shear")

    @property
    def tag(self):
        """Generate the pipeline's overall tag, which customizes the 'setup' folder the results are output to.
        """
        return (
            f"{conf.instance.setup_tag.get('mass', 'mass')}[{self.model_type}{self.mass_prior_model_tag}"
            f"{self.with_shear_tag}"
            f"{self.mass_centre_tag}]"
        )

    @property
    def shear_prior_model(self):
        """For a SLaM source pipeline, determine the shear model from the with_shear setting."""
        if not self.with_shear:
            return af.PriorModel(mp.ExternalShear)


class SetupMassLightDark(setup.SetupMassLightDark):
    def __init__(
        self,
        with_shear=True,
        mass_centre: (float, float) = None,
        constant_mass_to_light_ratio: bool = False,
        bulge_mass_to_light_ratio_gradient: bool = False,
        disk_mass_to_light_ratio_gradient: bool = False,
        align_light_dark_centre: bool = False,
        align_bulge_dark_centre: bool = False,
    ):
        """The setup of mass modeling in a pipeline, which controls how PyAutoLens template pipelines runs, for
        example controlling assumptions about the mass-to-light profile used too control how a light profile is
        converted to a mass profile.

        Users can write their own pipelines which do not use or require the *SetupPipeline* class.

        This class enables pipeline tagging, whereby the setup of the pipeline is used in the template pipeline
        scripts to tag the output path of the results depending on the setup parameters. This allows one to fit
        different models to a dataset in a structured path format.

        Parameters
        ----------
        mass_centre : (float, float)
           If input, a fixed (y,x) centre of the mass profile is used which is not treated as a free parameter by the
           non-linear search.
        align_bulge_mass_centre : bool
            If True, and the mass model is a decomposed single light and dark matter model (e.g. EllipticalSersic +
            SphericalNFW), the centre of the light and dark matter profiles are aligned.
        constant_mass_to_light_ratio : bool
            If True, and the mass model consists of multiple `LightProfile` and `MassProfile` coomponents, the
            mass-to-light ratio's of all components are fixed to one shared value.
        bulge_mass_to_light_ratio_gradient : bool
            If True, the bulge `EllipticalSersic` component of the mass model is altered to include a gradient in its
            mass-to-light ratio conversion.
        disk_mass_to_light_ratio_gradient : bool
            If True, the bulge `EllipticalExponential` component of the mass model is altered to include a gradient in
            its mass-to-light ratio conversion.
        align_bulge_mass_centre : bool
            If True, and the mass model is a bulge and dark matter modoel (e.g. EllipticalSersic + SphericalNFW),
            the centre of the bulge and dark matter profiles are aligned.
        align_bulge_mass_centre : bool
            If True, and the mass model is a decomposed bulge, disk and dark matter model (e.g. EllipticalSersic +
            EllipticalExponential + SphericalNFW), the centre of the bulge and dark matter profiles are aligned.
        """
        super().__init__(
            mass_centre=mass_centre,
            constant_mass_to_light_ratio=constant_mass_to_light_ratio,
            bulge_mass_to_light_ratio_gradient=bulge_mass_to_light_ratio_gradient,
            disk_mass_to_light_ratio_gradient=disk_mass_to_light_ratio_gradient,
            align_light_dark_centre=align_light_dark_centre,
            align_bulge_dark_centre=align_bulge_dark_centre,
        )

        self.with_shear = with_shear

    @property
    def tag(self):
        """Generate the pipeline's overall tag, which customizes the 'setup' folder the results are output to.
        """
        return (
            f"{conf.instance.setup_tag.get('mass', 'mass')}[{self.model_type}"
            f"{self.mass_centre_tag}"
            f"{self.with_shear_tag}"
            f"{self.mass_to_light_tag}"
            f"{self.align_light_dark_centre_tag}"
            f"{self.align_bulge_dark_centre_tag}]"
        )

    @property
    def with_shear_tag(self):
        """Generate a tag if an `ExternalShear` is included in the mass model of the pipeline  are
        fixedto a previous estimate, or varied during the analysis, to customize pipeline output paths..

        For the the default configuration files `config/notation/setup_tags.ini` tagging is performed as follows:

        with_shear = `False` -> setup__with_shear
        with_shear = `True` -> setup___with_shear
        """
        if not self.with_shear:
            return "__" + conf.instance.setup_tag.get("mass", "with_shear")
        return "__" + conf.instance.setup_tag.get("mass", "with_shear")

    @property
    def mass_centre_tag(self):
        """Generate a tag if the lens mass model centre of the pipeline is fixed to an input value, to customize
        pipeline output paths.

        For the the default configuration files `config/notation/setup_tags.ini` tagging is performed as follows:

        mass_centre = None -> setup
        mass_centre = (1.0, 1.0) -> setup___mass_centre_(1.0, 1.0)
        mass_centre = (3.0, -2.0) -> setup___mass_centre_(3.0, -2.0)
        """
        if self.mass_centre is None:
            return ""

        y = "{0:.2f}".format(self.mass_centre[0])
        x = "{0:.2f}".format(self.mass_centre[1])
        return (
            "__"
            + conf.instance.setup_tag.get("mass", "mass_centre")
            + "_("
            + y
            + ","
            + x
            + ")"
        )

    @property
    def shear_prior_model(self):
        """For a SLaM source pipeline, determine the shear model from the with_shear setting."""
        if not self.with_shear:
            return af.PriorModel(mp.ExternalShear)


class SetupSourceInversion(setup.SetupSourceInversion):
    def __init__(
        self,
        pixelization: pix.Pixelization = None,
        regularization: reg.Regularization = None,
        inversion_pixels_fixed: float = None,
    ):
        """The setup of the source modeling of a pipeline, which controls how PyAutoGalaxy template pipelines runs,
        for example controlling the `Pixelization` and `Regularization` used by a source model which uses an
        `Inversion`.

        Users can write their own pipelines which do not use or require the *SetupSourceParametric* class.

        This class enables pipeline tagging, whereby the setup of the pipeline is used in the template pipeline
        scripts to tag the output path of the results depending on the setup parameters. This allows one to fit
        different models to a dataset in a structured path format.

        Parameters
        ----------
        pixelization : pix.Pixelization or None
           If the pipeline uses an `Inversion` to reconstruct the galaxy's light, this determines the
           `Pixelization` used.
        regularization : reg.Regularization or None
           If the pipeline uses an `Inversion` to reconstruct the galaxy's light, this determines the
           `Regularization` scheme used.
        inversion_pixels_fixed : float
            The fixed number of source pixels used by a `Pixelization` class that takes as input a fixed number of
            pixels.
        """

        super().__init__(
            pixelization=pixelization,
            regularization=regularization,
            inversion_pixels_fixed=inversion_pixels_fixed,
        )


class SetupSubhalo:
    def __init__(
        self,
        subhalo_search: af.NonLinearSearch = None,
        source_is_model: bool = True,
        mass_is_model: bool = True,
        grid_size: int = 5,
        parallel: bool = False,
        subhalo_instance=None,
    ):
        """The setup of a subhalo pipeline, which controls how PyAutoLens template pipelines runs.

        Users can write their own pipelines which do not use or require the *SetupPipeline* class.

        This class enables pipeline tagging, whereby the setup of the pipeline is used in the template pipeline
        scripts to tag the output path of the results depending on the setup parameters. This allows one to fit
        different models to a dataset in a structured path format.

        Parameters
        ----------
        subhalo_instance : ag.MassProfile
            An instance of the mass-profile used as a fixed model for a subhalo pipeline.
        """

        if subhalo_search is None:
            subhalo_search = af.DynestyStatic(n_live_points=50, walks=5, facc=0.2)

        self.subhalo_search = subhalo_search
        self.source_is_model = source_is_model
        self.mass_is_model = mass_is_model
        self.grid_size = grid_size
        self.parallel = parallel
        self.subhalo_instance = subhalo_instance

    @property
    def model_type(self):
        return "nfw"

    @property
    def tag(self):
        return (
            f"{conf.instance.setup_tag.get('subhalo', 'subhalo')}[{self.model_type}"
            f"{self.mass_is_model_tag}"
            f"{self.source_is_model_tag}"
            f"{self.grid_size_tag}"
            f"{self.subhalo_centre_tag}"
            f"{self.subhalo_mass_at_200_tag}]"
        )

    @property
    def mass_is_model_tag(self):
        if self.mass_is_model:
            return f"__{conf.instance.setup_tag.get('subhalo', 'mass_is_model')}"
        return f"__{conf.instance.setup_tag.get('subhalo', 'mass_is_instance')}"

    @property
    def source_is_model_tag(self):
        if self.source_is_model:
            return f"__{conf.instance.setup_tag.get('subhalo', 'source_is_model')}"
        return f"__{conf.instance.setup_tag.get('subhalo', 'source_is_instance')}"

    @property
    def subhalo_centre_tag(self):
        """Generate a tag if the subhalo mass model centre of the pipeline is fixed to an input value, to customize
        pipeline output paths.

        For the the default configuration files `config/notation/setup_tags.ini` tagging is performed as follows:

        subhalo_centre = None -> setup
        subhalo_centre = (1.0, 1.0) -> setup___sub_centre_(1.0, 1.0)
        subhalo_centre = (3.0, -2.0) -> setup___sub_centre_(3.0, -2.0)
        """
        if self.subhalo_instance is None:
            return ""
        else:
            y = "{0:.2f}".format(self.subhalo_instance.centre[0])
            x = "{0:.2f}".format(self.subhalo_instance.centre[1])
            return (
                "__"
                + conf.instance.setup_tag.get("subhalo", "subhalo_centre")
                + "_("
                + y
                + ","
                + x
                + ")"
            )

    @property
    def grid_size_tag(self):
        return f"__{conf.instance.setup_tag.get('subhalo', 'grid_size')}_{str(self.grid_size)}"

    @property
    def subhalo_mass_at_200_tag(self):
        """Generate a tag if the subhalo mass model mass_at_200 of the pipeline is fixed to an input value, to
        customize pipeline output paths.

        For the the default configuration files `config/notation/setup_tags.ini` tagging is performed as follows:

        subhalo_mass_at_200 = None -> setup
        subhalo_mass_at_200 = 1e8 -> setup___sub_mass_1.0e+08
        subhalo_mass_at_200 = 1e9 -> setup___sub_mass_1.0e+09
        """
        if self.subhalo_instance is None:
            return ""
        else:

            return (
                "__"
                + conf.instance.setup_tag.get("subhalo", "mass_at_200")
                + "_"
                + "{0:.1e}".format(self.subhalo_instance.mass_at_200)
            )


class SetupPipeline(setup.SetupPipeline):
    def __init__(
        self,
        path_prefix: str = None,
        redshift_lens: float = 0.5,
        redshift_source: float = 1.0,
        setup_hyper: setup.SetupHyper = None,
        setup_light: setup.AbstractSetupLight = None,
        setup_mass: setup.AbstractSetupMass = None,
        setup_source: setup.AbstractSetupSource = None,
        setup_smbh: setup.SetupSMBH = None,
        subhalo: SetupSubhalo = None,
    ):
        """
        The setup of a ``Pipeline``, which controls how **PyAutoLens** template pipelines runs, for example controlling
        assumptions about the bulge-disk model or the model used to fit the source galaxy.

        Users can write their own pipelines which do not use or require the *SetupPipeline* class.

        This class enables pipeline tagging, whereby the setup of the pipeline is used in the template pipeline
        scripts to tag the output path of the results depending on the setup parameters. This allows one to fit
        different models to a dataset in a structured path format.

        Parameters
        ----------
        path_prefix : str or None
            The prefix of folders between the output path of the pipeline and the pipeline name, tags and phase folders.
        redshift_lens : float
            The redshift of the lens galaxy used by the pipeline for converting arc-seconds to kpc, masses to solMass,
            etc.
        redshift_source : float
            The redshift of the source galaxy used by the pipeline for converting arc-seconds to kpc, masses to solMass,
            etc.
        setup_hyper : SetupHyper
            The setup of the hyper analysis if used (e.g. hyper-galaxy noise scaling).
        setup_source : SetupSourceInversion
            The setup of the source analysis (e.g. the _Pixelization and _Regularization used).
        setup_light : SetupLightParametric
            The setup of the light profile modeling (e.g. for bulge-disk models if they are geometrically aligned).
        setup_mass : SetupMassTotal or SetupMassLightDark
            The setup of the mass modeling (e.g. if a constant mass to light ratio is used).
        setup_smbh : SetupSMBH
            The setup of a SMBH in the mass model, if included.
        subhalo : SetupSubhalo
            The setup of a subhalo in the mass model, if included.
        """

        super().__init__(
            path_prefix=path_prefix,
            redshift_source=redshift_source,
            setup_hyper=setup_hyper,
            setup_source=setup_source,
            setup_light=setup_light,
            setup_mass=setup_mass,
            setup_smbh=setup_smbh,
        )

        self.redshift_lens = redshift_lens
        self.subhalo = subhalo

    @property
    def tag(self):
        """Generate the pipeline's overall tag, which customizes the 'setup' folder the results are output to.
        """

        setup_tag = conf.instance.setup_tag.get("pipeline", "pipeline")
        hyper_tag = f"__{self.setup_hyper.tag}" if self.setup_hyper is not None else ""
        source_tag = (
            f"__{self.setup_source.tag}" if self.setup_source is not None else ""
        )
        light_tag = f"__{self.setup_light.tag}" if self.setup_light is not None else ""
        mass_tag = f"__{self.setup_mass.tag}" if self.setup_mass is not None else ""
        smbh_tag = f"__{self.setup_smbh.tag}" if self.setup_smbh is not None else ""
        subhalo_tag = f"__{self.subhalo.tag}" if self.subhalo is not None else ""

        return f"{setup_tag}{hyper_tag}{light_tag}{mass_tag}{smbh_tag}{subhalo_tag}{source_tag}"
