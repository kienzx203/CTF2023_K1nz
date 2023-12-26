#!/bin/bash

# Kiểm tra xem có tệp JAR nào không
shopt -s nullglob

# Duyệt qua tất cả các tệp JAR trong thư mục hiện tại
for jar_file in *.jar; do
  echo "Extracting content from $jar_file..."
  
  # Tạo một thư mục con với tên tương tự tệp JAR để trích xuất nội dung
  folder_name="${jar_file%.*}"
  mkdir -p "$folder_name"
  
  # Trích xuất nội dung từ tệp JAR vào thư mục con
  jar xf "$jar_file" -C "$folder_name"
  
  echo "Extraction from $jar_file completed."
done

echo "Extraction completed for all JAR files."
