# Flask Backend API Server for Barcode Scanning and LangChain Instruction Handling

Current API Endpoint, hosting at: https://hammerhead-app-qlv3d.ondigitalocean.app/

This repository contains the code for a custom API server designed to facilitate barcode scanning using PyZbar and instruction handling through LangChain. The purpose of this server is to provide users with a simple and efficient way to scan barcodes and receive relevant instructions based on the scanned data.

The server is built using the Flask framework, which offers a lightweight and flexible environment for building web applications in Python. Flask allows us to handle incoming HTTP requests and provide appropriate responses.

## Getting Started

To begin using this API server for barcode scanning and LangChain instruction handling, follow these steps:

1. Clone this repository to your local machine.

2. Install the required dependencies by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the server by executing the command:

   ```bash
   python main.py
   ```

## API Endpoints

### `POST /`

This endpoint accepts an image URL of a barcode as a parameter, sends a request to the LangChain API for instruction processing, and returns the generated instructions along with additional product details and search results.

#### Input Payload

The `POST /` endpoint expects the following parameter to be included in the request body:

- `image_url`: The URL of the image containing the barcode to be scanned.

#### Output Format

The response from the `POST /scan-barcode` endpoint will be a JSON object with the following format:

```json
{
    "product": {
        "barcode": 8936111962451,
        "price": 0,
        "publisher": "Công ty Cổ phần Dược phẩm SANTEX",
        "title": "An kinh Pasteur Hộp 01 lọ/ lọ 30 viên nang cứng"
    },
    "search_result": [
        {
            "link": "https://soyte.haugiang.gov.vn/media/1197/tai-lieu-kien-thuc-attp-cho-nguoi-san-xuat-thuc-pham-dv-an-uong.pdf",
            "provider": "soyte.haugiang.gov.vn",
            "title": "TÀI LIỆU TẬP HUẤN KIẾN THỨC VỀ AN TOÀN THỰC PHẨM"
        },
        {
            "link": "https://dmec.moh.gov.vn/documents/10182/32875499/upload_00130751_1658475459386.pdf?version=1.0&fileId=32906018",
            "provider": "dmec.moh.gov.vn",
            "title": "Phoenix™ M50 Sách hướng dẫn sử dụng hệ thống máy định danh ..."
        },
        // ... additional search results ...
    ],
    "status": "success"
}
```

The `product` object contains details about the scanned product, the `search_result` array contains related search results, and the `status` field indicates the success status of the request.

## Deployment

To deploy this API server, you can follow similar deployment strategies as those used for Flask applications. Make sure to configure environment variables and settings according to your deployment environment.

## Future Enhancements

The API server for barcode scanning and LangChain instruction handling has potential for future improvements:

- **Error Handling**: Implement robust error handling mechanisms to provide informative responses for different scenarios.

- **Enhanced Data Extraction**: Expand the data extracted from the barcode to provide more comprehensive product details.

- **User Authentication**: Introduce user authentication mechanisms if personalized instructions are needed.

- **Integration with External Services**: Extend the search result mechanism to retrieve information from various external sources.

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyZbar Documentation](https://github.com/NaturalHistoryMuseum/pyzbar)
- [LangChain Documentation](https://langchain-docs.example.com)

For more detailed information and support, refer to the documentation provided for each technology.