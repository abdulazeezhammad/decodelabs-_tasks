{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f783311c-cfea-4a61-97c7-ac5d59e0bba7",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Feature Engineering (Constructing 3 new predictive features)\n",
    "# Feature A: Gross Revenue before discount application\n",
    "df['Gross_Revenue'] = df['Price Per Unit'] * df['Quantity']\n",
    "\n",
    "# Feature B: Calculated value of the discount applied\n",
    "df['Discount_Amount'] = df['Gross_Revenue'] * (df['Discount Applied'] / 100)\n",
    "\n",
    "# Feature C: Average spend profile per single unit ordered\n",
    "df['Spend_Per_Unit'] = df['Total Spent'] / (df['Quantity'] + 1e-5) # 1e-5 prevents division by zero\n",
    "\n",
    "# 2. Collinearity Check\n",
    "# Grouping features to check for mathematical redundancy\n",
    "numeric_features = ['Price Per Unit', 'Quantity', 'Total Spent', 'Discount Applied', \n",
    "                    'Gross_Revenue', 'Discount_Amount', 'Spend_Per_Unit']\n",
    "\n",
    "# Generate and display the absolute correlation matrix\n",
    "corr_matrix = df[numeric_features].corr().abs()\n",
    "print(\"\\n=== ABSOLUTE CORRELATION MATRIX ===\")\n",
    "print(corr_matrix)"
   ]
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
