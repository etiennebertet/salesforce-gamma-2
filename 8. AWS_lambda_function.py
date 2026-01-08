import json
import urllib.request
import ftplib
import os
import tempfile
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Parse incoming data from Salesforce
    body = json.loads(event['body'])
    image_url = body.get('imageUrl')
    csv_data = body.get('csvData')
    salesforce_id = body.get('salesforceId')
    
    debug_messages = []
    status = "success"
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 1. Process Image
        if image_url:
            try:
                image_path = os.path.join(temp_dir, 'image.jpg')
                urllib.request.urlretrieve(image_url, image_path)
                debug_messages.append("Image URL retrieved successfully")
            except Exception as e:
                debug_messages.append(f"Failed to retrieve image: {str(e)}")
                status = "partial_failure"
        
        # 2. Process CSV
        if csv_data:
            try:
                csv_path = os.path.join(temp_dir, 'data.csv')
                with open(csv_path, 'w') as f:
                    f.write(csv_data)
                debug_messages.append("CSV data processed successfully")
            except Exception as e:
                debug_messages.append(f"Failed to process CSV data: {str(e)}")
                status = "partial_failure"
        
        # 3. FTP Transfer
        try:
            ftp = ftplib.FTP(os.environ['FTP_HOST'])
            ftp.login(os.environ['FTP_USER'], os.environ['FTP_PASS'])
            debug_messages.append("FTP connection established successfully")
            
            # Transfer image if exists
            if image_url and os.path.exists(image_path):
                try:
                    with open(image_path, 'rb') as f:
                        ftp.storbinary(f'STOR image_{salesforce_id}.jpg', f)
                    debug_messages.append("Image transferred successfully")
                except Exception as e:
                    debug_messages.append(f"Image transfer failed: {str(e)}")
                    status = "partial_failure"
            
            # Transfer CSV if exists
            if csv_data and os.path.exists(csv_path):
                try:
                    with open(csv_path, 'rb') as f:
                        ftp.storbinary(f'STOR data_{salesforce_id}.csv', f)
                    debug_messages.append("CSV transferred successfully")
                except Exception as e:
                    debug_messages.append(f"CSV transfer failed: {str(e)}")
                    status = "partial_failure"
            
            ftp.quit()
        except Exception as e:
            debug_messages.append(f"FTP connection failed: {str(e)}")
            status = "failure"
        
    finally:
        # Clean up files
        try:
            if image_url and os.path.exists(image_path):
                os.remove(image_path)
                debug_messages.append("Image file deleted")
        except Exception as e:
            debug_messages.append(f"Failed to delete image file: {str(e)}")
        
        try:
            if csv_data and os.path.exists(csv_path):
                os.remove(csv_path)
                debug_messages.append("CSV file deleted")
        except Exception as e:
            debug_messages.append(f"Failed to delete CSV file: {str(e)}")
        
        # Remove temp directory
        try:
            os.rmdir(temp_dir)
        except:
            pass
    
    # Prepare response
    response = {
        "status": status,
        "message": "\n".join(debug_messages),
        "salesforceId": salesforce_id
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }