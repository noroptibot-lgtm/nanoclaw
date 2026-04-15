# Computer Vision (Senior Computer Vision Engineer)

## Overview

The Computer Vision skill provides comprehensive tools and frameworks for building advanced image processing, object detection, segmentation, and visual recognition systems. This skill enables computer vision engineers to develop state-of-the-art CV pipelines using OpenCV, PyTorch, TensorFlow, and modern architectures like YOLO, SAM, and CLIP. It combines model training, inference optimization, and deployment with deep expertise in image processing techniques and deep learning for vision tasks.

## Who Should Use This Skill

- **Computer Vision Engineers** building visual AI systems
- **Senior CV Researchers** implementing cutting-edge algorithms
- **ML Engineers** specializing in vision tasks
- **Robotics Engineers** implementing perception systems
- **AI Engineers** working on multimodal applications
- **Data Scientists** analyzing visual data
- **Research Scientists** developing new CV techniques
- **Tech Leads** architecting vision pipelines

## Purpose and Use Cases

Use this skill when you need to:
- Build object detection and tracking systems
- Implement image segmentation and classification
- Create facial recognition and analysis systems
- Develop optical character recognition (OCR) pipelines
- Build pose estimation and activity recognition
- Implement 3D reconstruction and depth estimation
- Create visual search and similarity systems
- Build medical image analysis pipelines
- Implement video analysis and understanding
- Create augmented reality vision systems
- Build autonomous vehicle perception
- Implement quality inspection systems

**Keywords that trigger this skill:** computer vision, OpenCV, object detection, image segmentation, YOLO, SAM, image processing, CNN, visual recognition, facial recognition, OCR, pose estimation, video analysis

## What's Included

### Vision Pipeline Generator

**Pipeline Templates:**
- **Object Detection Pipeline** - YOLO, DETR, Faster R-CNN
- **Segmentation Pipeline** - SAM, Mask R-CNN, U-Net
- **Classification Pipeline** - ResNet, EfficientNet, ViT
- **Face Recognition Pipeline** - FaceNet, ArcFace, DeepFace
- **OCR Pipeline** - Tesseract, EasyOCR, TrOCR
- **Pose Estimation Pipeline** - MediaPipe, OpenPose, HRNet
- **Tracking Pipeline** - SORT, DeepSORT, ByteTrack
- **3D Vision Pipeline** - NeRF, depth estimation, stereo vision

**Generation Features:**
```bash
# Generate object detection pipeline
python scripts/vision_pipeline_generator.py object_detection \
  --model yolov8 \
  --classes person,car,bicycle \
  --input-source camera \
  --with-tracking \
  --export-onnx

# Generate segmentation pipeline
python scripts/vision_pipeline_generator.py segmentation \
  --model sam \
  --task instance \
  --with-refinement \
  --optimize-inference

# Generate classification pipeline
python scripts/vision_pipeline_generator.py classification \
  --model efficientnet-b3 \
  --num-classes 100 \
  --with-data-augmentation \
  --with-gradcam

# Generate face recognition pipeline
python scripts/vision_pipeline_generator.py face_recognition \
  --model facenet \
  --detection-model retinaface \
  --with-alignment \
  --with-liveness-detection
```

**Generated Pipeline Structure:**
```python
# pipelines/object_detection/detector.py
import cv2
import torch
from ultralytics import YOLO
from typing import List, Dict, Tuple
import numpy as np

class ObjectDetector:
    """YOLOv8 Object Detection Pipeline"""

    def __init__(
        self,
        model_path: str = "yolov8n.pt",
        confidence_threshold: float = 0.25,
        iou_threshold: float = 0.45,
        device: str = "cuda",
    ):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.device = device
        self.model.to(device)

    def preprocess(self, image: np.ndarray) -> torch.Tensor:
        """Preprocess image for inference"""
        # Resize while maintaining aspect ratio
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def detect(self, image: np.ndarray) -> List[Dict]:
        """
        Detect objects in image

        Returns:
            List of detections with format:
            {
                'bbox': [x1, y1, x2, y2],
                'class': str,
                'confidence': float,
                'class_id': int
            }
        """
        results = self.model(
            image,
            conf=self.confidence_threshold,
            iou=self.iou_threshold,
            device=self.device,
        )

        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                detection = {
                    'bbox': box.xyxy[0].cpu().numpy().tolist(),
                    'class': self.model.names[int(box.cls[0])],
                    'confidence': float(box.conf[0]),
                    'class_id': int(box.cls[0]),
                }
                detections.append(detection)

        return detections

    def visualize(
        self,
        image: np.ndarray,
        detections: List[Dict],
        show_labels: bool = True,
    ) -> np.ndarray:
        """Draw bounding boxes and labels on image"""
        vis_image = image.copy()

        for det in detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            confidence = det['confidence']
            class_name = det['class']

            # Draw bounding box
            cv2.rectangle(vis_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Draw label
            if show_labels:
                label = f"{class_name}: {confidence:.2f}"
                cv2.putText(
                    vis_image,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

        return vis_image

    def batch_detect(self, images: List[np.ndarray]) -> List[List[Dict]]:
        """Batch detection for multiple images"""
        return [self.detect(img) for img in images]

# pipelines/object_detection/tracker.py
from deep_sort_realtime.deepsort_tracker import DeepSort

class ObjectTracker:
    """Multi-object tracking using DeepSORT"""

    def __init__(self, max_age: int = 30):
        self.tracker = DeepSort(max_age=max_age)

    def update(self, detections: List[Dict], frame: np.ndarray) -> List[Dict]:
        """
        Update tracker with new detections

        Returns:
            List of tracked objects with IDs
        """
        # Convert detections to DeepSORT format
        detection_list = []
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            confidence = det['confidence']
            detection_list.append(([x1, y1, x2 - x1, y2 - y1], confidence, det['class']))

        # Update tracker
        tracks = self.tracker.update_tracks(detection_list, frame=frame)

        # Convert tracks back to our format
        tracked_objects = []
        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            bbox = track.to_ltrb()

            tracked_objects.append({
                'track_id': track_id,
                'bbox': bbox.tolist(),
                'class': track.det_class,
            })

        return tracked_objects

# pipelines/object_detection/pipeline.py
class DetectionPipeline:
    """Complete object detection and tracking pipeline"""

    def __init__(
        self,
        detector: ObjectDetector,
        tracker: ObjectTracker = None,
        input_source: str = "camera",
    ):
        self.detector = detector
        self.tracker = tracker
        self.input_source = input_source

    def process_video(
        self,
        video_path: str,
        output_path: str = None,
        show_preview: bool = False,
    ):
        """Process video with detection and tracking"""
        cap = cv2.VideoCapture(video_path if video_path != "camera" else 0)

        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Detect objects
            detections = self.detector.detect(frame)

            # Track objects if tracker is available
            if self.tracker:
                tracked_objects = self.tracker.update(detections, frame)
                # Visualize with track IDs
                vis_frame = self._visualize_tracks(frame, tracked_objects)
            else:
                vis_frame = self.detector.visualize(frame, detections)

            if output_path:
                out.write(vis_frame)

            if show_preview:
                cv2.imshow('Detection', vis_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        cap.release()
        if output_path:
            out.release()
        cv2.destroyAllWindows()

# tests/test_detector.py
import pytest
import numpy as np
from pipelines.object_detection.detector import ObjectDetector

def test_object_detector_initialization():
    detector = ObjectDetector()
    assert detector.confidence_threshold == 0.25
    assert detector.iou_threshold == 0.45

def test_object_detection():
    detector = ObjectDetector()
    # Create dummy image
    image = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    detections = detector.detect(image)
    assert isinstance(detections, list)

    if len(detections) > 0:
        det = detections[0]
        assert 'bbox' in det
        assert 'class' in det
        assert 'confidence' in det
        assert len(det['bbox']) == 4

def test_batch_detection():
    detector = ObjectDetector()
    images = [np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8) for _ in range(3)]
    results = detector.batch_detect(images)
    assert len(results) == 3
    assert all(isinstance(r, list) for r in results)
```

### Image Processing Toolkit

**Processing Operations:**
- Image enhancement (contrast, brightness, sharpening)
- Noise reduction and denoising
- Edge detection and corner detection
- Morphological operations
- Image filtering (Gaussian, median, bilateral)
- Color space conversions
- Geometric transformations
- Image pyramids and multi-scale processing

**Processing Features:**
```bash
# Enhance image quality
python scripts/image_processor.py enhance \
  --input image.jpg \
  --operations denoise,sharpen,contrast \
  --output enhanced.jpg

# Extract features
python scripts/image_processor.py extract_features \
  --input image.jpg \
  --method sift,orb,harris \
  --visualize

# Batch processing
python scripts/image_processor.py batch \
  --input-dir images/ \
  --operations resize:640x640,normalize \
  --output-dir processed/
```

**Processing Examples:**
```python
# Image enhancement pipeline
from cv_toolkit import ImageEnhancer

enhancer = ImageEnhancer()

# Denoise
denoised = enhancer.denoise(image, method='bilateral')

# Enhance contrast
enhanced = enhancer.enhance_contrast(denoised, method='clahe')

# Sharpen
sharpened = enhancer.sharpen(enhanced, kernel_size=5)

# Auto white balance
balanced = enhancer.auto_white_balance(sharpened)

# Edge detection
from cv_toolkit import EdgeDetector

detector = EdgeDetector()
edges = detector.canny(image, threshold1=50, threshold2=150)
```

### Model Training Framework

**Training Capabilities:**
- Custom dataset preparation and augmentation
- Transfer learning from pretrained models
- Multi-GPU training support
- Mixed precision training (FP16)
- Experiment tracking (Weights & Biases, MLflow)
- Hyperparameter optimization
- Model evaluation and validation
- Export to ONNX, TensorRT, CoreML

**Training Features:**
```bash
# Train object detection model
python scripts/train_model.py \
  --task detection \
  --model yolov8m \
  --data config/dataset.yaml \
  --epochs 100 \
  --batch-size 16 \
  --device cuda:0,cuda:1 \
  --mixed-precision \
  --augmentation heavy

# Train segmentation model
python scripts/train_model.py \
  --task segmentation \
  --model unet \
  --backbone resnet50 \
  --pretrained imagenet \
  --learning-rate 1e-4 \
  --scheduler cosine

# Fine-tune classification model
python scripts/train_model.py \
  --task classification \
  --model efficientnet-b3 \
  --checkpoint pretrained.pth \
  --freeze-backbone \
  --epochs 50
```

**Training Configuration:**
```yaml
# config/training.yaml
model:
  type: yolov8
  variant: medium
  pretrained: true

dataset:
  train: data/train
  val: data/val
  classes: ['person', 'car', 'bicycle']
  augmentation:
    - random_flip: 0.5
    - random_rotation: 15
    - color_jitter: [0.1, 0.1, 0.1]
    - random_crop: [0.8, 1.0]
    - mosaic: 0.5

training:
  epochs: 100
  batch_size: 16
  optimizer: adamw
  learning_rate: 1e-3
  weight_decay: 1e-4
  scheduler:
    type: cosine
    warmup_epochs: 5
  mixed_precision: true
  gradient_clip: 10.0

validation:
  interval: 5
  metrics: ['mAP', 'precision', 'recall']
  save_best: true

export:
  formats: ['onnx', 'tensorrt']
  optimize: true
```

### Model Optimization Toolkit

**Optimization Techniques:**
- Model pruning (structured and unstructured)
- Quantization (INT8, FP16)
- Knowledge distillation
- Neural architecture search
- ONNX optimization
- TensorRT conversion
- OpenVINO optimization
- Mobile optimization (TFLite, CoreML)

**Optimization Features:**
```bash
# Quantize model to INT8
python scripts/optimize_model.py quantize \
  --model model.pth \
  --calibration-data cal_images/ \
  --backend tensorrt \
  --output model_int8.engine

# Prune model
python scripts/optimize_model.py prune \
  --model model.pth \
  --sparsity 0.5 \
  --method structured \
  --fine-tune-epochs 10

# Convert to ONNX
python scripts/optimize_model.py convert \
  --model model.pth \
  --format onnx \
  --optimize \
  --input-shape 1,3,640,640
```

## How It Works

### Object Detection Workflow

**Step 1: Dataset Preparation**
```python
# Prepare YOLO format dataset
from cv_toolkit import DatasetConverter

converter = DatasetConverter()
converter.convert(
    input_format='coco',
    output_format='yolo',
    input_path='annotations.json',
    output_path='data/yolo/'
)

# Apply augmentation
from cv_toolkit import DataAugmenter

augmenter = DataAugmenter([
    'random_flip',
    'random_rotation:15',
    'random_brightness:0.2',
    'mosaic',
])

augmented_dataset = augmenter.augment_dataset(
    'data/yolo/',
    output_path='data/yolo_aug/',
    multiplier=3
)
```

**Step 2: Model Training**
```python
# Train YOLOv8 model
from ultralytics import YOLO

model = YOLO('yolov8m.pt')

results = model.train(
    data='config/dataset.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device=[0, 1],  # Multi-GPU
    workers=8,
    optimizer='AdamW',
    lr0=0.01,
    lrf=0.01,
    momentum=0.937,
    weight_decay=0.0005,
    warmup_epochs=3.0,
    box=7.5,
    cls=0.5,
    dfl=1.5,
    plots=True,
    save=True,
)

# Evaluate model
metrics = model.val()
print(f"mAP50: {metrics.box.map50:.3f}")
print(f"mAP50-95: {metrics.box.map:.3f}")
```

**Step 3: Model Optimization**
```python
# Export to ONNX with optimization
model.export(
    format='onnx',
    optimize=True,
    simplify=True,
    dynamic=False,
    opset=12,
)

# Convert to TensorRT
import tensorrt as trt

engine = model.export(
    format='engine',
    half=True,  # FP16
    workspace=4,  # 4GB workspace
    device=0,
)

# Benchmark performance
from cv_toolkit import ModelBenchmark

benchmark = ModelBenchmark()
results = benchmark.run(
    model='model.engine',
    input_shape=(1, 3, 640, 640),
    num_runs=100,
)
print(f"Latency: {results['latency_mean']:.2f}ms")
print(f"FPS: {results['fps']:.1f}")
```

**Step 4: Deployment**
```python
# Create inference pipeline
from cv_toolkit import InferencePipeline

pipeline = InferencePipeline(
    model='model.engine',
    device='cuda:0',
    batch_size=1,
)

# Process video stream
for frame in video_stream:
    detections = pipeline.infer(frame)
    visualized = pipeline.visualize(frame, detections)
    output_stream.write(visualized)
```

### Segmentation Workflow

**Step 1: Prepare Segmentation Data**
```python
# Convert masks to COCO format
from cv_toolkit import SegmentationDataset

dataset = SegmentationDataset.from_masks(
    image_dir='images/',
    mask_dir='masks/',
    num_classes=21,
)

# Split dataset
train_set, val_set = dataset.split(train_ratio=0.8)
```

**Step 2: Train Segmentation Model**
```python
# Train U-Net with ResNet50 backbone
import segmentation_models_pytorch as smp
import pytorch_lightning as pl

model = smp.Unet(
    encoder_name='resnet50',
    encoder_weights='imagenet',
    in_channels=3,
    classes=21,
)

# Create Lightning module
class SegmentationModel(pl.LightningModule):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.loss_fn = smp.losses.DiceLoss(mode='multiclass')

    def training_step(self, batch, batch_idx):
        images, masks = batch
        logits = self.model(images)
        loss = self.loss_fn(logits, masks)
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-4)

# Train
trainer = pl.Trainer(
    max_epochs=100,
    gpus=2,
    precision=16,
    accelerator='ddp',
)
trainer.fit(model, train_dataloader, val_dataloader)
```

**Step 3: Inference and Post-processing**
```python
# Segment image
def segment_image(model, image):
    # Preprocess
    image_tensor = preprocess(image)

    # Inference
    with torch.no_grad():
        logits = model(image_tensor)
        pred_mask = torch.argmax(logits, dim=1)

    # Post-process
    mask = pred_mask.cpu().numpy()[0]

    # Apply CRF for refinement
    from pydensecrf import densecrf
    refined_mask = apply_crf(image, mask)

    return refined_mask

# Visualize results
def visualize_segmentation(image, mask, classes):
    colored_mask = colorize_mask(mask, classes)
    overlay = cv2.addWeighted(image, 0.6, colored_mask, 0.4, 0)
    return overlay
```

## Technical Details

### Deep Learning Architectures

**Object Detection:**
- **YOLO (v5-v8):** Fast single-stage detectors
- **DETR:** Transformer-based detection
- **Faster R-CNN:** Two-stage detector with high accuracy
- **RetinaNet:** Focal loss for handling class imbalance
- **EfficientDet:** Efficient scaling of detectors

**Segmentation:**
- **U-Net:** Medical image segmentation
- **DeepLab v3+:** Atrous convolutions for semantic segmentation
- **Mask R-CNN:** Instance segmentation
- **SAM (Segment Anything):** Zero-shot segmentation
- **SegFormer:** Transformer-based segmentation

**Classification:**
- **ResNet:** Deep residual networks
- **EfficientNet:** Compound scaling
- **Vision Transformer (ViT):** Attention-based classification
- **ConvNeXt:** Modern ConvNet architecture
- **Swin Transformer:** Hierarchical vision transformer

### Inference Optimization

**TensorRT Optimization:**
```python
import tensorrt as trt

def build_engine(onnx_path, engine_path):
    logger = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(logger)
    network = builder.create_network(
        1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    )
    parser = trt.OnnxParser(network, logger)

    # Parse ONNX
    with open(onnx_path, 'rb') as model:
        parser.parse(model.read())

    # Build engine with FP16
    config = builder.create_builder_config()
    config.set_flag(trt.BuilderFlag.FP16)
    config.max_workspace_size = 4 << 30  # 4GB

    engine = builder.build_engine(network, config)

    # Save engine
    with open(engine_path, 'wb') as f:
        f.write(engine.serialize())

    return engine
```

**ONNX Runtime Optimization:**
```python
import onnxruntime as ort

# Create optimized session
sess_options = ort.SessionOptions()
sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
sess_options.intra_op_num_threads = 4

providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
session = ort.InferenceSession(
    'model.onnx',
    sess_options,
    providers=providers
)

# Run inference
input_name = session.get_inputs()[0].name
output = session.run(None, {input_name: input_data})
```

### Image Processing Algorithms

**Edge Detection:**
```python
# Canny edge detection
edges = cv2.Canny(image, threshold1=50, threshold2=150, apertureSize=3)

# Sobel edge detection
sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
magnitude = np.sqrt(sobelx**2 + sobely**2)
```

**Feature Detection:**
```python
# SIFT features
sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(image, None)

# ORB features (faster alternative)
orb = cv2.ORB_create(nfeatures=1000)
keypoints, descriptors = orb.detectAndCompute(image, None)

# Feature matching
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
matches = bf.match(descriptors1, descriptors2)
```

## Best Practices

### Model Development Best Practices

**Do:**
- Start with pretrained models (transfer learning)
- Use data augmentation to prevent overfitting
- Validate on separate test set
- Monitor metrics during training
- Use mixed precision for faster training
- Implement early stopping
- Save model checkpoints regularly
- Version control datasets and models

**Don't:**
- Train from scratch without trying transfer learning
- Ignore class imbalance in datasets
- Overfit to training data
- Skip validation metrics
- Use single train/test split
- Forget to normalize inputs
- Ignore inference speed requirements
- Deploy without testing edge cases

### Data Preparation Best Practices

**Do:**
- Clean and validate annotations
- Balance class distributions
- Use stratified splits
- Apply appropriate augmentations
- Normalize image inputs
- Handle different image sizes properly
- Create data pipelines with caching
- Document data preprocessing steps

**Don't:**
- Use low-quality or mislabeled data
- Apply excessive augmentation
- Leak test data into training
- Ignore data distribution shifts
- Use inappropriate augmentations
- Forget to version datasets
- Mix different data sources without normalization

### Inference Optimization Best Practices

**Do:**
- Profile model performance
- Use appropriate batch sizes
- Optimize for target hardware
- Use FP16 when possible
- Implement model caching
- Use asynchronous inference
- Monitor memory usage
- Benchmark against requirements

**Don't:**
- Deploy unoptimized models
- Ignore latency requirements
- Use excessive model complexity
- Forget about memory constraints
- Skip hardware-specific optimizations
- Ignore thermal throttling on edge devices
- Deploy without load testing

## Integration Points

This skill integrates with:
- **Deep Learning:** PyTorch, TensorFlow, JAX, ONNX Runtime
- **Vision Libraries:** OpenCV, Pillow, scikit-image, albumentations
- **Model Frameworks:** Ultralytics, MMDetection, Detectron2, Segmentation Models
- **Optimization:** TensorRT, OpenVINO, ONNX, TFLite
- **MLOps:** Weights & Biases, MLflow, DVC, ClearML
- **Deployment:** FastAPI, TorchServe, TensorFlow Serving, Triton
- **Hardware:** NVIDIA GPUs, Intel CPUs, ARM processors, Google Coral
- **Cloud:** AWS SageMaker, Google Cloud Vision, Azure Computer Vision

## Common Challenges and Solutions

### Challenge: Poor Model Accuracy
**Solution:** Use larger pretrained models, increase dataset size, apply better augmentation, tune hyperparameters, handle class imbalance, validate annotations quality, use ensemble methods

### Challenge: Slow Inference Speed
**Solution:** Model quantization (INT8), TensorRT optimization, reduce input resolution, use lighter models, implement batching, use asynchronous inference, optimize pre/post-processing

### Challenge: High Memory Usage
**Solution:** Reduce batch size, use gradient checkpointing, implement model pruning, use FP16 precision, optimize data loading, use memory-efficient architectures, implement streaming inference

### Challenge: Domain Shift / Poor Generalization
**Solution:** Use domain adaptation techniques, augment with target domain data, fine-tune on target domain, use robust feature extractors, implement test-time augmentation, collect more diverse training data

### Challenge: Real-time Processing Requirements
**Solution:** Use optimized models (YOLO, EfficientDet), deploy on GPU/TPU, implement frame skipping, use motion detection for preprocessing, optimize entire pipeline, use edge devices with NPU

### Challenge: Handling Varied Image Quality
**Solution:** Implement adaptive preprocessing, train with diverse data quality, use robust normalization, implement quality assessment, apply denoising as preprocessing, use multi-scale processing
