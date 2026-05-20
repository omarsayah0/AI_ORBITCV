from src.utils import load_config, prepare_dataframe
from src.train import run_training
from src.dataset import CloudDataset
from src.inference import run_inference

#use pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 
# instead of pip uninstall torch torchvision torchaudio that is going to be in the pyproject.toml if you cant find cuda.
def main():
    config = load_config("configs/config.yaml")

    mode = "train"

    if mode == "train":
        run_training(config)

    elif mode == "inference":
        df = prepare_dataframe(config["paths"]["data_csv"])

        dataset = CloudDataset(
            df=df,
            data_dir=config["paths"]["data_dir"],
            image_size=config["data"]["image_size"],
            classes=config["data"]["classes"],
            transform=None
        )

        run_inference(config, dataset, index=0)


if __name__ == "__main__":
    main()