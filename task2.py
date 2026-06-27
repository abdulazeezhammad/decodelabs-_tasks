{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "60b96bb4-b867-453a-a062-6ce91c6f188d",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Convert categorical features into numerical orthogonal coordinate space\n",
    "df = pd.get_dummies(df, columns=['Item'], drop_first=True, dtype=int)\n",
    "\n",
    "# Verifying the changes by printing the new columns\n",
    "print(\"=== NEWLY ENCODED COLUMNS ===\")\n",
    "print(df.columns)"
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
