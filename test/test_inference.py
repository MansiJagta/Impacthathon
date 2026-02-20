from indian_id_validator.inference import process_id

result = process_id(
    image_path="test/test_license_1.jpeg",
    save_json=False
)

print(result)
