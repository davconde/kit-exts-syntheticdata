import omni.replicator.core as rep
import omni.graph.core as og
import os


def generate(models):
    with rep.new_layer('Replicator'):
        NUCLEUS = models["assets"]["nucleus_path"].get_value_as_string()
        ASSETS = NUCLEUS + models["assets"]["objects_path"].get_value_as_string()
        ENVS = NUCLEUS + models["assets"]["envs_path"].get_value_as_string()

        # TODO Parametrize
        def populate(size=models["assets"]["max_instances"].get_value_as_int()):
            def mod_assets(instances, obj_class):
                with instances:
                    rep.modify.semantics([('class', obj_class)])
                    objs = models["objects"]
                    rep.modify.pose(
                        position=rep.distribution.uniform(
                            (objs["loc"]["min"]["x"].get_value_as_float(),
                            objs["loc"]["min"]["y"].get_value_as_float(),
                            objs["loc"]["min"]["z"].get_value_as_float()),
                            (objs["loc"]["max"]["x"].get_value_as_float(),
                            objs["loc"]["max"]["y"].get_value_as_float(),
                            objs["loc"]["max"]["z"].get_value_as_float())),
                        rotation=rep.distribution.uniform(
                            (objs["rot"]["min"]["x"].get_value_as_float(),
                            objs["rot"]["min"]["y"].get_value_as_float(),
                            objs["rot"]["min"]["z"].get_value_as_float()),
                            (objs["rot"]["max"]["x"].get_value_as_float(),
                            objs["rot"]["max"]["y"].get_value_as_float(),
                            objs["rot"]["max"]["z"].get_value_as_float())),
                    )
            # TODO Parametrize
            classes = {'car': 2, 'motorcycle': 3, 'truck': 7}
            for key, value in classes.items():
                instances = rep.randomizer.instantiate(
                    rep.utils.get_usd_files(f"{ASSETS}/{key}", recursive=True),
                    size=size//len(classes),
                    mode='scene_instance')
                mod_assets(instances, value)
                
            return instances.node

        # Register randomization
        rep.randomizer.register(populate)

        # Setup the static elements
        if models["assets"]["use_envs"].get_value_as_bool():
            env = rep.create.from_usd(ENVS)

        # Setup camera and attach it to render product
        camera = rep.create.camera(
            focal_length=models["camera"]["focal_length"].get_value_as_float(),
            focus_distance=models["camera"]["focus_distance"].get_value_as_float(),
            f_stop=models["camera"]["f_stop"].get_value_as_float()
        )
        render_product = rep.create.render_product(
            camera,
            resolution=(models["resolution"]["width"].get_value_as_int(),
                        models["resolution"]["height"].get_value_as_int()))

        # Initialize and attach writer
        # TODO Isolate from BasicWriter
        if models["annotators"]["KITTI"].get_value_as_bool() or models["annotators"]["YOLO"].get_value_as_bool():
            kittiWriter = rep.WriterRegistry.get("KittiWriter")
            kittiWriter.initialize(
                output_dir=models["annotators"]["output_dir"].get_value_as_string() + "/kitti_writer/",
                bbox_height_threshold=5,
                fully_visible_threshold=0.75,
                omit_semantic_type=True)
            kittiWriter.attach([render_product])
        else:
            writer = rep.WriterRegistry.get("BasicWriter")
            writer.initialize(
                output_dir=models["annotators"]["output_dir"].get_value_as_string(),
                rgb=models["annotators"]["RGB"].get_value_as_bool(),
                normals=models["annotators"]["normals"].get_value_as_bool(),
                bounding_box_2d_loose=models["annotators"]["BBox2D_loose"].get_value_as_bool(),
                bounding_box_2d_tight=models["annotators"]["BBox2D_tight"].get_value_as_bool(),
                bounding_box_3d=models["annotators"]["BBox3D"].get_value_as_bool(),
                distance_to_camera=models["annotators"]["dist_cam"].get_value_as_bool(),
                distance_to_image_plane=models["annotators"]["dist_img"].get_value_as_bool(),
                semantic_segmentation=models["annotators"]["semantic_seg"].get_value_as_bool(),
                instance_id_segmentation=models["annotators"]["instance_id_seg"].get_value_as_bool(),
                instance_segmentation=models["annotators"]["instance_seg"].get_value_as_bool(),
                pointcloud=models["annotators"]["point_cloud"].get_value_as_bool(),
                skeleton_data=models["annotators"]["skeleton"].get_value_as_bool(),
                motion_vectors=models["annotators"]["motion_vec"].get_value_as_bool(),
                camera_params=models["annotators"]["cam_param"].get_value_as_bool()
                )
            writer.attach([render_product])

        cam_attrs = models["camera"]
        with rep.trigger.on_frame(num_frames=models["num_frames"].get_value_as_int()):
            rep.randomizer.populate(models["assets"]["max_instances"].get_value_as_int())
            with camera:
                rep.modify.pose(
                    position=rep.distribution.uniform(
                        (cam_attrs["loc"]["min"]["x"].get_value_as_float(),
                         cam_attrs["loc"]["min"]["y"].get_value_as_float(),
                         cam_attrs["loc"]["min"]["z"].get_value_as_float()),
                        (cam_attrs["loc"]["max"]["x"].get_value_as_float(),
                         cam_attrs["loc"]["max"]["y"].get_value_as_float(),
                         cam_attrs["loc"]["max"]["z"].get_value_as_float())),
                    look_at=rep.distribution.uniform(
                        (cam_attrs["lookat"]["min"]["x"].get_value_as_float(),
                         cam_attrs["lookat"]["min"]["y"].get_value_as_float(),
                         cam_attrs["lookat"]["min"]["z"].get_value_as_float()),
                        (cam_attrs["lookat"]["max"]["x"].get_value_as_float(),
                         cam_attrs["lookat"]["max"]["y"].get_value_as_float(),
                         cam_attrs["lookat"]["max"]["z"].get_value_as_float())))


def preview():
    rep.orchestrator.preview()


def run():
    rep.orchestrator.run()
