import omni.ui as ui
from .replicator import generate, preview, run
from .utils import load_models_dict, save_models_dict, dict_primitives_to_models
from .style import sdg_style
import carb


MODELS_PLACEHOLDER = 'infrarob'

class SDGWindow(ui.Window):
    def __init__(self, title: str, **kwargs) -> None:
        super().__init__(title, **kwargs)
        self._models = {}
        self._build_models(model='default')
        self._build_window()

    def _build_models(self, model):
        self._models = load_models_dict(model=model)
        dict_primitives_to_models(self._models)
        self._models["config_file"] = ui.SimpleStringModel(MODELS_PLACEHOLDER)

    def _build_window(self):
        with self.frame:
            with ui.ScrollingFrame():
                with ui.VStack(style=sdg_style):
                    with ui.VStack(height=0):
                        ui.Label("Parameters", style={"font_size": 18})
                        with ui.HStack(spacing=5):
                            ui.Label("Config file")
                            ui.StringField(model=self._models["config_file"])
                            ui.Button("Load", clicked_fn=self._on_loadConfig)
                            ui.Button("Save", clicked_fn=self._on_saveConfig)
                        with ui.HStack(spacing=5):
                            ui.Label("Resolution Width", width=ui.Percent(25))
                            ui.IntField(model=self._models["resolution"]["width"], width=ui.Percent(25))
                            ui.Label("Resolution Height", width=ui.Percent(25))
                            ui.IntField(model=self._models["resolution"]["height"], width=ui.Percent(25))
                        with ui.HStack(spacing=5):
                            ui.Label("Number of Frames", width=ui.Percent(25))
                            ui.IntField(model=self._models["num_frames"], width=ui.Percent(75))
                        with ui.CollapsableFrame("Assets"):
                            with ui.VStack():
                                with ui.HStack(spacing=5):
                                    ui.Label("Nucleus Path")
                                    ui.StringField(model=self._models["assets"]["nucleus_path"],
                                                   width=ui.Percent(75))
                                with ui.HStack(spacing=5):
                                    ui.Label("Objects Path")
                                    ui.StringField(model=self._models["assets"]["objects_path"],
                                                   width=ui.Percent(75))
                                with ui.HStack(spacing=5):
                                    ui.Label("Envs Path")
                                    ui.StringField(model=self._models["assets"]["envs_path"],
                                                   width=ui.Percent(75))
                                with ui.HStack(spacing=5):
                                    ui.Label("Use Envs")
                                    ui.CheckBox(model=self._models["assets"]["use_envs"],
                                                width=ui.Percent(75))
                                with ui.HStack(spacing=5):
                                    ui.Label("Min Instances")
                                    ui.IntField(model=self._models["assets"]["min_instances"])
                                    ui.Label("Max Instances")
                                    ui.IntField(model=self._models["assets"]["max_instances"])
                        with ui.CollapsableFrame("Camera"):
                            with ui.VStack():
                                with ui.HStack(spacing=5):
                                    ui.Label("Focal Length")
                                    ui.FloatField(model=self._models["camera"]["focal_length"], width=ui.Percent(75))
                                with ui.HStack(spacing=5):
                                    ui.Label("Focus Distance")
                                    ui.FloatField(model=self._models["camera"]["focus_distance"], width=ui.Percent(75))
                                with ui.HStack(spacing=5):
                                    ui.Label("F Stop")
                                    ui.FloatField(model=self._models["camera"]["f_stop"], width=ui.Percent(75))
                                with ui.HStack(spacing=5):
                                    ui.Label("Min Location")
                                    ui.FloatField(model=self._models["camera"]["loc"]["min"]["x"])
                                    ui.FloatField(model=self._models["camera"]["loc"]["min"]["y"])
                                    ui.FloatField(model=self._models["camera"]["loc"]["min"]["z"])
                                with ui.HStack(spacing=5):
                                    ui.Label("Max Location")
                                    ui.FloatField(model=self._models["camera"]["loc"]["max"]["x"])
                                    ui.FloatField(model=self._models["camera"]["loc"]["max"]["y"])
                                    ui.FloatField(model=self._models["camera"]["loc"]["max"]["z"])
                                with ui.HStack(spacing=5):
                                    ui.Label("Min Look At")
                                    ui.FloatField(model=self._models["camera"]["lookat"]["min"]["x"])
                                    ui.FloatField(model=self._models["camera"]["lookat"]["min"]["y"])
                                    ui.FloatField(model=self._models["camera"]["lookat"]["min"]["z"])
                                with ui.HStack(spacing=5):
                                    ui.Label("Max Look At")
                                    ui.FloatField(model=self._models["camera"]["lookat"]["max"]["x"])
                                    ui.FloatField(model=self._models["camera"]["lookat"]["max"]["y"])
                                    ui.FloatField(model=self._models["camera"]["lookat"]["max"]["z"])
                        with ui.CollapsableFrame("Objects"):
                            with ui.VStack():
                                with ui.HStack(spacing=5):
                                    ui.Label("Min Location")
                                    ui.FloatField(model=self._models["objects"]["loc"]["min"]["x"])
                                    ui.FloatField(model=self._models["objects"]["loc"]["min"]["y"])
                                    ui.FloatField(model=self._models["objects"]["loc"]["min"]["z"])
                                with ui.HStack(spacing=5):
                                    ui.Label("Max Location")
                                    ui.FloatField(model=self._models["objects"]["loc"]["max"]["x"])
                                    ui.FloatField(model=self._models["objects"]["loc"]["max"]["y"])
                                    ui.FloatField(model=self._models["objects"]["loc"]["max"]["z"])
                                with ui.HStack(spacing=5):
                                    ui.Label("Min Rotation")
                                    ui.FloatField(model=self._models["objects"]["rot"]["min"]["x"])
                                    ui.FloatField(model=self._models["objects"]["rot"]["min"]["y"])
                                    ui.FloatField(model=self._models["objects"]["rot"]["min"]["z"])
                                with ui.HStack(spacing=5):
                                    ui.Label("Max Rotation")
                                    ui.FloatField(model=self._models["objects"]["rot"]["max"]["x"])
                                    ui.FloatField(model=self._models["objects"]["rot"]["max"]["y"])
                                    ui.FloatField(model=self._models["objects"]["rot"]["max"]["z"])
                        with ui.CollapsableFrame("Annotators"):
                            with ui.VStack():
                                with ui.HStack(spacing=5):
                                    ui.Label("Output Directory",
                                             tooltip=r"Windows root on <drive>:\Users\<user>\omni.replicator_out")
                                    ui.StringField(model=self._models["annotators"]["output_dir"],
                                                   width=ui.Percent(75))
                                with ui.HStack(spacing=5):
                                    ui.Label("RGB")
                                    ui.CheckBox(model=self._models["annotators"]["RGB"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Normals")
                                    ui.CheckBox(model=self._models["annotators"]["normals"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Bounding Box 2D Loose")
                                    ui.CheckBox(model=self._models["annotators"]["BBox2D_loose"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Bounding Box 2D Tight")
                                    ui.CheckBox(model=self._models["annotators"]["BBox2D_tight"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Bounding Box 3D")
                                    ui.CheckBox(model=self._models["annotators"]["BBox3D"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Distance to Camera")
                                    ui.CheckBox(model=self._models["annotators"]["dist_cam"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Distance to Image Plane")
                                    ui.CheckBox(model=self._models["annotators"]["dist_img"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Semantic Segmentation")
                                    ui.CheckBox(model=self._models["annotators"]["semantic_seg"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Instance ID Segmentation")
                                    ui.CheckBox(model=self._models["annotators"]["instance_id_seg"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Instance Segmentation")
                                    ui.CheckBox(model=self._models["annotators"]["instance_seg"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Point Cloud")
                                    ui.CheckBox(model=self._models["annotators"]["point_cloud"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Skeleton Data")
                                    ui.CheckBox(model=self._models["annotators"]["skeleton"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Motion Vectors")
                                    ui.CheckBox(model=self._models["annotators"]["motion_vec"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("Camera Parameters")
                                    ui.CheckBox(model=self._models["annotators"]["cam_param"],
                                                width=ui.Percent(50))
                                with ui.HStack(spacing=5):
                                    ui.Label("KITTI")
                                    ui.CheckBox(model=self._models["annotators"]["KITTI"],
                                                width=ui.Percent(50))
                        ui.Line()
                    with ui.VStack(height=0):
                        ui.Label("Status", style={"font_size": 18})
                        self._status_label = ui.Label("Click on Generate Graph to start")
                        ui.Line()
                    with ui.HStack(height=0):
                        ui.Button("Generate Graph", clicked_fn=self._on_generateClick)
                        ui.Button("Preview", clicked_fn=self._on_previewClick)
                        ui.Button("Run", clicked_fn=self._on_runClick)

    def _on_generateClick(self):
        generate(self._models)
        self._status_label.text = "Graph generated"

    def _on_previewClick(self):
        preview()

    def _on_runClick(self):
        run()
        self._status_label.text = "Data saved"

    def _on_loadConfig(self):
        config_file = self._models["config_file"].get_value_as_string()
        self._build_models(model=config_file)
        self._build_window()

    def _on_saveConfig(self):
        config_file = self._models["config_file"].get_value_as_string()
        save_models_dict(self._models, model=config_file)

    def destroy(self):
        super().destroy()
        self._models = None
