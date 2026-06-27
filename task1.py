{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "20c5f00a-2760-48d3-9087-1d742c3d988e",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "from sklearn.impute import KNNImputer"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "c2eb2563-95f3-4458-9881-42827fa6d4a1",
   "metadata": {},
   "outputs": [],
   "source": [
    "df = pd.read_csv('retail_store_sales.csv')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "6657fdde-4a71-46f9-b325-1e38a9c7f2df",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(12575, 11)"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Checking the numbers of colums and rowns \n",
    "df.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "292eb142-73da-4fb5-a24b-df7ee09b12e4",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Transaction ID         0\n",
       "Customer ID            0\n",
       "Category               0\n",
       "Item                1213\n",
       "Price Per Unit       609\n",
       "Quantity             604\n",
       "Total Spent          604\n",
       "Payment Method         0\n",
       "Location               0\n",
       "Transaction Date       0\n",
       "Discount Applied    4199\n",
       "dtype: int64"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Checking for the total number of missing value in each cloumn\n",
    "df.isnull().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "aacbf269-87bd-4332-9822-a0bf35fcbb09",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "=== MISSING DATA AUDIT ===\n",
      "                  Missing Count  Percentage Missing (%)\n",
      "Discount Applied           4199               33.391650\n",
      "Item                       1213                9.646123\n",
      "Price Per Unit              609                4.842942\n",
      "Quantity                    604                4.803181\n",
      "Total Spent                 604                4.803181\n"
     ]
    }
   ],
   "source": [
    "# Converting the the total missing values in each column to Percentage\n",
    "missing_pct = (df.isnull().sum() / len(df)) * 100\n",
    "\n",
    "# Creating a report dataframe\n",
    "report = pd.DataFrame({\n",
    "    'Missing Count': df.isnull().sum(),\n",
    "    'Percentage Missing (%)': missing_pct\n",
    "})\n",
    "\n",
    "# Displaying columns that have missing values, sorted from highest to lowest\n",
    "print(\"=== MISSING DATA AUDIT ===\")\n",
    "print(report[report['Missing Count'] > 0].sort_values(by='Percentage Missing (%)', ascending=False))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "308854bb-7ae3-45de-a400-79ccffce0c0a",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "from sklearn.impute import KNNImputer\n",
    "\n",
    "# 1. Drop rows for columns under 5% missingness\n",
    "low_missing_cols = ['Price Per Unit', 'Quantity', 'Total Spent']\n",
    "df = df.dropna(subset=low_missing_cols)\n",
    "\n",
    "# 2. Impute with Mode for 'Item' (Categorical, between 5% and 20%)\n",
    "item_mode = df['Item'].mode()[0]\n",
    "df['Item'] = df['Item'].fillna(item_mode)\n",
    "\n",
    "# 3. Apply KNN Imputation for 'Discount Applied' (Over 20%)\n",
    "knn_cols = ['Price Per Unit', 'Quantity', 'Total Spent', 'Discount Applied']\n",
    "imputer = KNNImputer(n_neighbors=5)\n",
    "df[knn_cols] = imputer.fit_transform(df[knn_cols])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "29ac24d9-ae88-455d-a52c-d2e0e95a7b9a",
   "metadata": {},
   "outputs": [],
   "source": [
    "# List of numeric columns to handle outliers\n",
    "numeric_cols = ['Price Per Unit', 'Quantity', 'Total Spent', 'Discount Applied']\n",
    "\n",
    "for col in numeric_cols:\n",
    "    Q1 = df[col].quantile(0.25)\n",
    "    Q3 = df[col].quantile(0.75)\n",
    "    IQR = Q3 - Q1\n",
    "    \n",
    "    lower_bound = Q1 - 1.5 * IQR\n",
    "    upper_bound = Q3 + 1.5 * IQR\n",
    "    \n",
    "    # Cap values outside the statistical boundaries\n",
    "    df[col] = np.clip(df[col], lower_bound, upper_bound)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "691eeb7a-6433-428b-b28c-90e2ecaca686",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "anaconda-2025.12-py312",
   "language": "python",
   "name": "conda-env-anaconda-2025.12-py312-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
