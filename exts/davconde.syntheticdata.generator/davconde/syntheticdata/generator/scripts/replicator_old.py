import omni.replicator.core as rep
import omni.graph.core as og
from . import options


def generate():
    with rep.new_layer('Replicator'):
        # Define paths for the character, the props, the environment
        # and the surface where the assets will be scattered in.

        NUCLEUS = 'omniverse://localhost/'
        ASSETS = NUCLEUS + 'Library/Assets/'
        NVIDIA_ASSETS = NUCLEUS + 'NVIDIA/Assets/'

        VEHICLE = ASSETS + 'Vehicles/Fiat_Punto_GT.usdz'
        VEHICLES = ASSETS + 'Vehicles_Instanceable'
        PROPS = ASSETS + 'Vegetation/Shrub'
        ENVS = ASSETS + 'Scenes/Templates/Road/Road.usd'
        # ENVS = NVIDIA_ASSETS + 'Scenes/Templates/Outdoor/Puddles.usd'

        '''
        POPULATE PROPS
                    position=rep.distribution.combine((
                        rep.distribution.uniform(
                            (-1000, 0, -1000), (-500, 0, -500)
                        ),
                        rep.distribution.uniform(
                            (500, 0, 500), (1000, 0, 1000)
                        ))),
        '''

        # Define randomizer function for Base assets.
        # This randomization includes placement and rotation
        # of the assets on the surface.
        def env_props(size=options.REPLICATOR['INSTANCES_NUM']):
            instances = rep.randomizer.instantiate(
                rep.utils.get_usd_files(VEHICLES, recursive=True),
                size=size,
                mode='scene_instance')
            with instances:
                rep.modify.semantics([('class', 'vehicle')])
                rep.modify.pose(
                    position=rep.distribution.uniform(
                        (-1000, 0, -1500), (1000, 0, -250)),
                    rotation=rep.distribution.uniform(
                        (0, -180, 0), (0, 180, 0)),
                )
            return instances.node

        def vehicle():
            vehicle = rep.create.from_usd(
                VEHICLE,
                semantics=[('class', 'vehicle')])

            with vehicle:
                rep.modify.pose(
                    position=rep.distribution.uniform(
                        (0, 0, 0), (500, 0, 500)),
                    rotation=rep.distribution.uniform(
                        (0, -45, 0), (0, 45, 0)),
                )
            return vehicle

        # Register randomization
        rep.randomizer.register(env_props)
        rep.randomizer.register(vehicle)

        # Setup the static elements
        if options.REPLICATOR['USE_ENV']:
            env = rep.create.from_usd(ENVS)

        # Setup camera and attach it to render product
        camera = rep.create.camera(
            focus_distance=800,
            f_stop=0.5
        )
        render_product = rep.create.render_product(
            camera,
            resolution=(1024, 1024))

        # Initialize and attach writer
        writer = rep.WriterRegistry.get("BasicWriter")
        writer.initialize(
            output_dir="_output",
            rgb=True,
            bounding_box_2d_tight=True)
        writer.attach([render_product])

        with rep.trigger.on_frame(num_frames=10):
            rep.randomizer.env_props(options.REPLICATOR['INSTANCES_NUM'])
            # rep.randomizer.vehicle()

            with camera:
                rep.modify.pose(
                    position=rep.distribution.uniform(
                        (-500, 200, 1000), (500, 500, 1500)),
                    look_at=(0, 0, 0))


def preview():
    rep.orchestrator.preview()


def run():
    rep.orchestrator.run()
