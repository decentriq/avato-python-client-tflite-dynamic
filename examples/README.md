# avato-tflite-dynamic-demo

## Installation 

### Prerequisites

You need to have Python >=3.6 installed (check using `python --version`) and internet access.

### Installation

1. Create a new Python environment to install into using
   `python -m venv .env`
2. Activate the environment using
   `source .env/bin/activate`
3. Install all dependencies using `.env/bin/pip install -r requirements.txt`

### Run Demo

Make sure you have the correct Python environment activated. If you just installed the module, it's already set. Otherwise you may have to run `source .env/bin/activate` again.

Set the trial user credentials via

```
export MODEL_OWNER_API_TOKEN="#PLACEHOLDER#"
export INFERENCE_USER_API_TOKEN="#PLACEHOLDER#"
export INFERENCE_USER_ID="#PLACEHOLDER#"
```

To run the demo, start a Jupyter notebook server with `.env/bin/jupyter notebook` which should open a browser window. In the browser window, open the `tflite_demo_model_owner.ipynb` notebook to train and confidentially deploy a model to Azure. Then open the `tflite_demo_inference_user.ipynb` notebook to perform confidential inference on the model.
