While setting this project in your Salesforce org, add the following Apex classes and connect them with a schedule or automated flow so that they can be launched one after the other. 

Be sure to set the API keys of your own accounts in the Salesforce Secure Credentials storage and allow the URL to be reached out by your org (Check URL security settings)  

You must create a custom object that is going to be used to store the data in custom fields. 

The first class generates a text prompt and stores it in a field. 

The second class generate a text that will be exported as a .csv file when calling to the AWS Lambda Python script.

The third class uses the previous prompt to generate an image by calling an AI.

The fourth class uses the same prompt to generate the image filename.

The fifth class updates the CSV metadata with the new filename.

The sixth class Upscale the image to be compliant with the hosting websites requirements.

The seventh class calls a python function hosted on AWS Lambda 

The AWS Lambda file 1.Hosts the upscaled image on S3 Bucket ; 2.Exports the CSV text into a .csv file on S3 Bucket ; 3.Launches a FTP transfer to a specialized hosting server (Shutterstock, Freepik, Adibe Cloud, etc.)

