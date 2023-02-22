import boto3
import json
import os

# Set the endpoint name and client
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
client = boto3.client(service_name='sagemaker-runtime')


# Transform input test data
def transform(data):
    try:
        feature = data.copy()
        
        if feature[1] == "Male":
            feature[1] = "1"
        else:
            feature[1] = "0"

        if feature[2] == "Yes":
            feature[2] = "1"
        else:
            feature[2] = "0"

        if feature[3] == "3+":
            feature[3] = "3"
        else:
            feature[3] = feature[3]

        if feature[4] == "Graduate":
            feature[4] = "1"
        else:
            feature[4] = "0"

        if feature[5] == "Yes":
            feature[5] = "1"
        else:
            feature[5] = "0"

        feature.extend(["0", "0", "0"])

        if feature[11] == "Rural":
            feature[12] = "1"
        elif feature[11] == "Semiurban":
            feature[13] = "1"
        elif feature[11] == "Urban":
            feature[14] = "1"
        feature.pop(11)
            
        return ','.join([str(f) for f in feature[1:]])
        
    except Exception as e:
        print('Error in transforming: {0},{1}'.format(data,e))
        raise Exception('Error in transforming: {0},{1}'.format(data,e))
        
    
def lambda_handler(event, context):
    try:    
        print("Event: " + json.dumps(event, indent=2))
        
        # Transform the input data
        test_data = json.loads(json.dumps(event))
        test_data = [transform(features["features"]) for features in test_data["data"]]
        
        # Invoke the predictions
        pred = client.invoke_endpoint(EndpointName=ENDPOINT_NAME, 
                               Body=('\n'.join(test_data).encode('utf-8')),
                               ContentType='text/csv')
                               
        pred = pred['Body'].read().decode('utf-8')
        pred = pred.split(',')
        predictions = [p for p in pred]
        
        return {
            'statusCode': 200,
            'isBase64Encoded':False,
            'body': json.dumps(predictions)
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'isBase64Encoded':False,
            'body': 'Call Failed {0}'.format(e)
        }
