# Common imports for KMRL AI Platform
import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import io
import time
import math
import threading
import queue
import json
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import requests
import os
import sys

# Machine Learning imports
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, VotingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, classification_report
from sklearn.cluster import KMeans, DBSCAN
from sklearn.svm import SVR, SVC
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA
import joblib
import warnings

# Advanced ML imports (with fallback)
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    print("XGBoost not available, using alternative models")

try:
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("TensorFlow not available, using alternative models")

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("Prophet not available, using alternative time series models")

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')
