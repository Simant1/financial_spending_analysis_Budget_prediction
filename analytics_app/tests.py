from django.test import TestCase
import pandas as pd
from .services.cleaning import clean_financial_data
from .services.transform import transform_financial_data
from .services.quality import assess_data_quality

class PipelineTests(TestCase):
    def test_pipeline(self):
        df = pd.DataFrame([{'date':'2025-01-01','description':'Tesco','category':'Food','amount':'45.2','type':'expense'}])
        q = assess_data_quality(df)
        cleaned = clean_financial_data(df)
        transformed = transform_financial_data(cleaned)
        self.assertEqual(q['missing_columns'], [])
        self.assertIn('month', transformed.columns)
