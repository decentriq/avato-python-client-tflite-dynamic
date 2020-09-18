# Examples

The examples are provided as Python Jupyter Notebooks.

## Prerequisites

You need to have Python >=3.6 installed (check using `python --version`) and internet access.

### Dependencies installation

1. Inside the current `examples` create a new Python environment using
   `python -m venv .env`
2. Activate the environment using
   `source .env/bin/activate`
3. Install all dependencies using `.env/bin/pip install -r requirements.txt`

### Run examples

Make sure you have the correct Python environment activated. If you just followed the instructions above it's already set. Otherwise you may have to run `source .env/bin/activate` again.
Set the trial user credentials via

```
export MODEL_OWNER_API_TOKEN="#PLACEHOLDER#"
export INFERENCE_USER_API_TOKEN="#PLACEHOLDER#"
export INFERENCE_USER_ID="#PLACEHOLDER#"
```
*N.B. These credentials are gonna be provided by decentriq*

To run the example, start a Jupyter notebook server with `.env/bin/jupyter notebook` which should open a browser window. In the browser window, open the `tflite_demo_model_owner.ipynb` notebook to train and confidentially deploy a model to Azure. Then open the `tflite_demo_inference_user.ipynb` notebook to perform confidential inference on the model.