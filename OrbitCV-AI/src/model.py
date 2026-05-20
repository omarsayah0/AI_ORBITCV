import torch.nn as nn
import segmentation_models_pytorch as smp


class UnetWithClassifier(nn.Module):
    def __init__(self, backbone, encoder_weights, num_classes):
        super().__init__()
        self.unet = smp.Unet(
            encoder_name=backbone,
            encoder_weights=encoder_weights,
            in_channels=3,
            classes=num_classes,
            activation=None,
        )
        encoder_out_channels = self.unet.encoder.out_channels[-1]
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Dropout(0.5),
            nn.Linear(encoder_out_channels, num_classes),
        )

    def forward(self, x):
        features = self.unet.encoder(x)
        try:
            decoder_output = self.unet.decoder(*features)
        except TypeError:
            decoder_output = self.unet.decoder(features)
        seg_output = self.unet.segmentation_head(decoder_output)
        cls_output = self.classifier(features[-1])
        return seg_output, cls_output

    @property
    def encoder(self):
        return self.unet.encoder

    @property
    def decoder(self):
        return self.unet.decoder

    @property
    def segmentation_head(self):
        return self.unet.segmentation_head


def build_model(config):
    backbone = config["model"]["backbone"]
    encoder_weights = "imagenet" if config["model"]["pretrained"] else None
    num_classes = len(config["data"]["classes"])
    return UnetWithClassifier(backbone, encoder_weights, num_classes)
