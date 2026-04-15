# Data Science (Senior Data Scientist)

## Overview

The Data Science skill provides comprehensive tools and frameworks for building machine learning models, conducting statistical analysis, and deriving insights from data using Python, R, and modern ML frameworks. This skill enables data scientists to perform exploratory data analysis, feature engineering, model training and evaluation, and deploy ML solutions. It combines statistical modeling, machine learning algorithms, experiment tracking, and model deployment with deep expertise in data analysis and predictive modeling.

## Who Should Use This Skill

- **Data Scientists** building ML models and analyzing data
- **Senior Data Scientists** architecting ML solutions
- **ML Engineers** deploying production ML systems
- **Research Scientists** conducting advanced analytics
- **Analytics Professionals** performing statistical analysis
- **Business Intelligence Analysts** building predictive models
- **Quantitative Analysts** performing statistical modeling
- **Tech Leads** establishing data science standards

## Purpose and Use Cases

Use this skill when you need to:
- Perform exploratory data analysis (EDA)
- Build predictive ML models
- Conduct statistical hypothesis testing
- Implement feature engineering pipelines
- Train deep learning models
- Perform time series forecasting
- Build recommendation systems
- Conduct A/B testing analysis
- Create data visualizations
- Implement model evaluation frameworks
- Deploy ML models to production
- Conduct causal inference analysis

**Keywords that trigger this skill:** data science, machine learning, ML, statistics, pandas, scikit-learn, TensorFlow, PyTorch, model training, feature engineering, EDA, predictive modeling, statistical analysis

## What's Included

### ML Project Generator

**Project Templates:**
- **Classification Project** - Binary/multi-class classification
- **Regression Project** - Linear/non-linear regression
- **Time Series Project** - Forecasting and anomaly detection
- **NLP Project** - Text classification, NER, sentiment analysis
- **Computer Vision Project** - Image classification, object detection
- **Recommendation System** - Collaborative/content-based filtering
- **Clustering Project** - K-means, hierarchical, DBSCAN
- **Anomaly Detection** - Outlier detection methods

**Generation Features:**
```bash
# Generate classification project
python scripts/ml_project_generator.py classification customer_churn \
  --framework scikit-learn \
  --with-eda \
  --with-feature-engineering \
  --with-hyperparameter-tuning \
  --with-mlflow-tracking

# Generate time series project
python scripts/ml_project_generator.py time-series sales_forecast \
  --framework prophet \
  --horizon 30 \
  --with-cross-validation \
  --with-visualization

# Generate deep learning project
python scripts/ml_project_generator.py deep-learning image_classifier \
  --framework pytorch \
  --architecture resnet \
  --with-data-augmentation \
  --with-tensorboard

# Generate full ML pipeline
python scripts/ml_project_generator.py pipeline recommendation_system \
  --with-feature-store \
  --with-model-registry \
  --with-monitoring \
  --deployment kubernetes
```

**Generated Project Structure:**
```python
# src/data/data_loader.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from typing import Tuple

class DataLoader:
    """Handle data loading and preprocessing"""

    def __init__(self, data_path: str, test_size: float = 0.2):
        self.data_path = data_path
        self.test_size = test_size

    def load_data(self) -> pd.DataFrame:
        """Load data from file"""
        if self.data_path.endswith('.csv'):
            return pd.read_csv(self.data_path)
        elif self.data_path.endswith('.parquet'):
            return pd.read_parquet(self.data_path)
        else:
            raise ValueError(f"Unsupported file format: {self.data_path}")

    def split_data(
        self,
        df: pd.DataFrame,
        target_col: str
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Split data into train and test sets"""

        X = df.drop(columns=[target_col])
        y = df[target_col]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=self.test_size,
            random_state=42,
            stratify=y  # For classification
        )

        return X_train, X_test, y_train, y_test

# src/features/feature_engineering.py
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd

class FeatureEngineer:
    """Feature engineering pipeline"""

    def __init__(self, numeric_features, categorical_features):
        self.numeric_features = numeric_features
        self.categorical_features = categorical_features
        self.preprocessor = None

    def create_pipeline(self) -> ColumnTransformer:
        """Create preprocessing pipeline"""

        numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numeric_features),
                ('cat', categorical_transformer, self.categorical_features)
            ]
        )

        self.preprocessor = preprocessor
        return preprocessor

    def fit_transform(self, X):
        """Fit and transform features"""
        if self.preprocessor is None:
            self.create_pipeline()
        return self.preprocessor.fit_transform(X)

    def transform(self, X):
        """Transform features"""
        return self.preprocessor.transform(X)

class CustomFeatureTransformer(BaseEstimator, TransformerMixin):
    """Custom feature transformations"""

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()

        # Create interaction features
        if 'age' in X.columns and 'income' in X.columns:
            X['age_income_ratio'] = X['age'] / (X['income'] + 1)

        # Create polynomial features
        if 'amount' in X.columns:
            X['amount_squared'] = X['amount'] ** 2
            X['amount_log'] = np.log1p(X['amount'])

        # Create time-based features
        if 'timestamp' in X.columns:
            X['hour'] = pd.to_datetime(X['timestamp']).dt.hour
            X['day_of_week'] = pd.to_datetime(X['timestamp']).dt.dayofweek
            X['is_weekend'] = X['day_of_week'].isin([5, 6]).astype(int)

        return X

# src/models/classifier.py
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)
import mlflow
import mlflow.sklearn
import numpy as np

class ChurnClassifier:
    """Customer churn classification model"""

    def __init__(self, model_type='random_forest'):
        self.model_type = model_type
        self.model = self._create_model()
        self.feature_importance = None

    def _create_model(self):
        """Create model based on type"""
        if self.model_type == 'random_forest':
            return RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == 'gradient_boosting':
            return GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        elif self.model_type == 'logistic_regression':
            return LogisticRegression(
                max_iter=1000,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

    def train(self, X_train, y_train, experiment_name='churn_prediction'):
        """Train model with MLflow tracking"""

        # Start MLflow run
        mlflow.set_experiment(experiment_name)

        with mlflow.start_run(run_name=f"{self.model_type}_model"):
            # Log parameters
            mlflow.log_params(self.model.get_params())

            # Train model
            self.model.fit(X_train, y_train)

            # Calculate feature importance
            if hasattr(self.model, 'feature_importances_'):
                self.feature_importance = self.model.feature_importances_

            # Log model
            mlflow.sklearn.log_model(self.model, "model")

        return self

    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""

        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
        }

        # Log metrics to MLflow
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)

        # Generate and log confusion matrix
        cm = confusion_matrix(y_test, y_pred)

        print("=" * 50)
        print("Model Evaluation Results")
        print("=" * 50)
        for metric, value in metrics.items():
            print(f"{metric.capitalize()}: {value:.4f}")

        print("\nConfusion Matrix:")
        print(cm)

        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        return metrics

    def predict(self, X):
        """Make predictions"""
        return self.model.predict(X)

    def predict_proba(self, X):
        """Predict probabilities"""
        return self.model.predict_proba(X)

    def get_feature_importance(self, feature_names, top_n=10):
        """Get top N most important features"""
        if self.feature_importance is None:
            return None

        importance_df = pd.DataFrame({
            'feature': feature_names,
            'importance': self.feature_importance
        }).sort_values('importance', ascending=False)

        return importance_df.head(top_n)

# src/models/hyperparameter_tuning.py
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class HyperparameterTuner:
    """Hyperparameter optimization"""

    def __init__(self, model, param_grid, cv=5, scoring='roc_auc'):
        self.model = model
        self.param_grid = param_grid
        self.cv = cv
        self.scoring = scoring
        self.best_model = None
        self.best_params = None
        self.best_score = None

    def grid_search(self, X_train, y_train):
        """Perform grid search"""

        grid_search = GridSearchCV(
            estimator=self.model,
            param_grid=self.param_grid,
            cv=self.cv,
            scoring=self.scoring,
            n_jobs=-1,
            verbose=2
        )

        grid_search.fit(X_train, y_train)

        self.best_model = grid_search.best_estimator_
        self.best_params = grid_search.best_params_
        self.best_score = grid_search.best_score_

        print(f"Best parameters: {self.best_params}")
        print(f"Best {self.scoring} score: {self.best_score:.4f}")

        return self.best_model

    def random_search(self, X_train, y_train, n_iter=50):
        """Perform randomized search"""

        random_search = RandomizedSearchCV(
            estimator=self.model,
            param_distributions=self.param_grid,
            n_iter=n_iter,
            cv=self.cv,
            scoring=self.scoring,
            n_jobs=-1,
            verbose=2,
            random_state=42
        )

        random_search.fit(X_train, y_train)

        self.best_model = random_search.best_estimator_
        self.best_params = random_search.best_params_
        self.best_score = random_search.best_score_

        return self.best_model

# Example parameter grids
RANDOM_FOREST_PARAMS = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt', 'log2'],
}

GRADIENT_BOOSTING_PARAMS = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'min_samples_split': [2, 5, 10],
    'subsample': [0.8, 0.9, 1.0],
}

# src/visualization/eda_plots.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class EDAVisualizer:
    """Exploratory data analysis visualizations"""

    def __init__(self, figsize=(12, 8)):
        self.figsize = figsize
        sns.set_style('whitegrid')

    def plot_distribution(self, df, columns, target=None):
        """Plot distribution of numeric features"""

        n_cols = len(columns)
        n_rows = (n_cols + 2) // 3

        fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5*n_rows))
        axes = axes.flatten() if n_cols > 1 else [axes]

        for idx, col in enumerate(columns):
            if target is not None:
                # Plot by target class
                for class_val in df[target].unique():
                    data = df[df[target] == class_val][col]
                    axes[idx].hist(data, alpha=0.5, label=f'{target}={class_val}', bins=30)
                axes[idx].legend()
            else:
                axes[idx].hist(df[col], bins=30, edgecolor='black')

            axes[idx].set_title(f'Distribution of {col}')
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel('Frequency')

        plt.tight_layout()
        return fig

    def plot_correlation_matrix(self, df, method='pearson'):
        """Plot correlation matrix heatmap"""

        numeric_cols = df.select_dtypes(include=[np.number]).columns
        corr_matrix = df[numeric_cols].corr(method=method)

        fig, ax = plt.subplots(figsize=self.figsize)
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True,
            ax=ax
        )
        ax.set_title(f'{method.capitalize()} Correlation Matrix')

        return fig

    def plot_feature_importance(self, feature_importance_df, top_n=20):
        """Plot feature importance"""

        fig, ax = plt.subplots(figsize=self.figsize)

        top_features = feature_importance_df.head(top_n)

        sns.barplot(
            data=top_features,
            x='importance',
            y='feature',
            ax=ax
        )

        ax.set_title(f'Top {top_n} Most Important Features')
        ax.set_xlabel('Importance')
        ax.set_ylabel('Feature')

        return fig

    def plot_roc_curve(self, y_true, y_pred_proba):
        """Plot ROC curve"""
        from sklearn.metrics import roc_curve, auc

        fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
        roc_auc = auc(fpr, tpr)

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.plot(fpr, tpr, color='darkorange', lw=2,
                label=f'ROC curve (AUC = {roc_auc:.2f})')
        ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--',
                label='Random Classifier')

        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('Receiver Operating Characteristic (ROC) Curve')
        ax.legend(loc="lower right")

        return fig

# main.py - Complete workflow
import argparse
from src.data.data_loader import DataLoader
from src.features.feature_engineering import FeatureEngineer
from src.models.classifier import ChurnClassifier
from src.models.hyperparameter_tuning import HyperparameterTuner, RANDOM_FOREST_PARAMS
from src.visualization.eda_plots import EDAVisualizer

def main():
    parser = argparse.ArgumentParser(description='Customer Churn Prediction')
    parser.add_argument('--data-path', required=True, help='Path to data file')
    parser.add_argument('--target-col', default='churn', help='Target column name')
    parser.add_argument('--model-type', default='random_forest',
                       choices=['random_forest', 'gradient_boosting', 'logistic_regression'])
    parser.add_argument('--tune-hyperparameters', action='store_true',
                       help='Perform hyperparameter tuning')
    args = parser.parse_args()

    # Load data
    print("Loading data...")
    loader = DataLoader(args.data_path)
    df = loader.load_data()
    X_train, X_test, y_train, y_test = loader.split_data(df, args.target_col)

    # Feature engineering
    print("Engineering features...")
    numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X_train.select_dtypes(include=['object']).columns.tolist()

    engineer = FeatureEngineer(numeric_features, categorical_features)
    X_train_processed = engineer.fit_transform(X_train)
    X_test_processed = engineer.transform(X_test)

    # Train model
    print(f"Training {args.model_type} model...")
    classifier = ChurnClassifier(model_type=args.model_type)

    if args.tune_hyperparameters:
        print("Tuning hyperparameters...")
        tuner = HyperparameterTuner(
            classifier.model,
            RANDOM_FOREST_PARAMS,
            cv=5,
            scoring='roc_auc'
        )
        classifier.model = tuner.grid_search(X_train_processed, y_train)

    classifier.train(X_train_processed, y_train)

    # Evaluate model
    print("Evaluating model...")
    metrics = classifier.evaluate(X_test_processed, y_test)

    # Visualizations
    print("Generating visualizations...")
    visualizer = EDAVisualizer()

    # Feature importance
    feature_names = (numeric_features +
                    engineer.preprocessor.named_transformers_['cat']
                    .named_steps['onehot'].get_feature_names_out(categorical_features).tolist())

    importance_df = classifier.get_feature_importance(feature_names, top_n=20)
    if importance_df is not None:
        fig = visualizer.plot_feature_importance(importance_df)
        plt.savefig('feature_importance.png')

    # ROC curve
    y_pred_proba = classifier.predict_proba(X_test_processed)[:, 1]
    fig = visualizer.plot_roc_curve(y_test, y_pred_proba)
    plt.savefig('roc_curve.png')

    print("Done! Check MLflow UI for detailed results.")

if __name__ == '__main__':
    main()
```

### Statistical Analysis Toolkit

**Analysis Types:**
- Hypothesis testing (t-tests, chi-square, ANOVA)
- A/B testing and experimentation
- Time series analysis
- Survival analysis
- Causal inference
- Bayesian statistics
- Regression analysis
- Non-parametric tests

**Implementation:**
```python
# Statistical hypothesis testing
from scipy import stats
import numpy as np

class StatisticalTester:
    """Statistical hypothesis testing"""

    @staticmethod
    def ttest_independent(group1, group2, alpha=0.05):
        """Independent t-test"""
        statistic, pvalue = stats.ttest_ind(group1, group2)

        result = {
            'test': 'Independent t-test',
            'statistic': statistic,
            'p_value': pvalue,
            'significant': pvalue < alpha,
            'alpha': alpha,
        }

        return result

    @staticmethod
    def ab_test(control, treatment, alpha=0.05):
        """A/B test for conversion rates"""

        n_control = len(control)
        n_treatment = len(treatment)
        conversions_control = sum(control)
        conversions_treatment = sum(treatment)

        rate_control = conversions_control / n_control
        rate_treatment = conversions_treatment / n_treatment

        # Z-test for proportions
        pooled_rate = (conversions_control + conversions_treatment) / (n_control + n_treatment)
        se = np.sqrt(pooled_rate * (1 - pooled_rate) * (1/n_control + 1/n_treatment))
        z_stat = (rate_treatment - rate_control) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

        # Calculate confidence interval
        ci_margin = 1.96 * se
        ci_lower = (rate_treatment - rate_control) - ci_margin
        ci_upper = (rate_treatment - rate_control) + ci_margin

        result = {
            'control_rate': rate_control,
            'treatment_rate': rate_treatment,
            'lift': (rate_treatment - rate_control) / rate_control * 100,
            'z_statistic': z_stat,
            'p_value': p_value,
            'significant': p_value < alpha,
            'confidence_interval': (ci_lower, ci_upper),
        }

        return result
```

### Model Deployment Framework

**Deployment Options:**
- REST API with Flask/FastAPI
- Batch prediction service
- Real-time inference server
- Model serving with TensorFlow Serving
- Serverless deployment (AWS Lambda)
- Container deployment (Docker/Kubernetes)

**Implementation:**
```python
# FastAPI model serving
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI(title="Churn Prediction API")

# Load model at startup
model = joblib.load('models/churn_model.pkl')
preprocessor = joblib.load('models/preprocessor.pkl')

class PredictionInput(BaseModel):
    features: dict

class PredictionOutput(BaseModel):
    prediction: int
    probability: float

@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: PredictionInput):
    try:
        # Convert to dataframe
        df = pd.DataFrame([input_data.features])

        # Preprocess
        X_processed = preprocessor.transform(df)

        # Predict
        prediction = model.predict(X_processed)[0]
        probability = model.predict_proba(X_processed)[0][1]

        return PredictionOutput(
            prediction=int(prediction),
            probability=float(probability)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

## Technical Details

### Feature Engineering Techniques

**Numeric Features:**
- Scaling (StandardScaler, MinMaxScaler, RobustScaler)
- Transformation (log, sqrt, Box-Cox, Yeo-Johnson)
- Binning and discretization
- Polynomial features
- Interaction features

**Categorical Features:**
- One-hot encoding
- Label encoding
- Target encoding
- Frequency encoding
- Embedding (for high cardinality)

**Time Features:**
- Extract datetime components
- Cyclic encoding (sin/cos)
- Time-based aggregations
- Lag features
- Rolling window statistics

### Model Selection and Evaluation

**Classification Metrics:**
- Accuracy, Precision, Recall, F1-score
- ROC-AUC, PR-AUC
- Confusion matrix
- Classification report

**Regression Metrics:**
- MAE, MSE, RMSE
- R-squared, Adjusted R-squared
- MAPE (Mean Absolute Percentage Error)

**Cross-Validation:**
- K-fold cross-validation
- Stratified K-fold
- Time series cross-validation
- Leave-one-out

## Best Practices

**Do:**
- Perform thorough EDA before modeling
- Split data properly (train/val/test)
- Use cross-validation for model selection
- Track experiments with MLflow/W&B
- Version control data and models
- Document assumptions and methodology
- Validate model on holdout set
- Monitor model performance in production
- Consider feature importance and interpretability
- Test for data leakage

**Don't:**
- Skip EDA and data quality checks
- Use test set for hyperparameter tuning
- Ignore class imbalance
- Overfit to training data
- Use metrics blindly without context
- Deploy models without monitoring
- Ignore feature engineering
- Forget to handle missing values
- Skip model documentation
- Ignore computational costs

## Integration Points

This skill integrates with:
- **ML Frameworks:** scikit-learn, XGBoost, LightGBM, CatBoost
- **Deep Learning:** PyTorch, TensorFlow, Keras, JAX
- **Experiment Tracking:** MLflow, Weights & Biases, Neptune
- **Feature Store:** Feast, Tecton, Hopsworks
- **Model Registry:** MLflow, DVC, Weights & Biases
- **Deployment:** FastAPI, Flask, TensorFlow Serving, Seldon
- **Monitoring:** Evidently AI, Whylabs, Arize
- **Notebooks:** Jupyter, Google Colab, Databricks

## Common Challenges and Solutions

### Challenge: Imbalanced Datasets
**Solution:** Use SMOTE/ADASYN for oversampling, random undersampling, class weights, stratified sampling, ensemble methods, anomaly detection approaches

### Challenge: Feature Selection
**Solution:** Use correlation analysis, feature importance from tree models, recursive feature elimination, L1 regularization, domain knowledge, PCA for dimensionality reduction

### Challenge: Overfitting
**Solution:** Use cross-validation, regularization (L1/L2), early stopping, dropout (neural networks), ensemble methods, increase training data, reduce model complexity

### Challenge: Model Interpretability
**Solution:** Use SHAP values, LIME, feature importance, partial dependence plots, simpler models when possible, model-agnostic explanation methods

### Challenge: Hyperparameter Tuning
**Solution:** Use grid search, random search, Bayesian optimization (Optuna, Hyperopt), automated ML tools, start with default parameters, use learning curves

### Challenge: Production Deployment
**Solution:** Containerize models, implement monitoring, version models, A/B test new models, implement rollback procedures, monitor data drift, automate retraining
