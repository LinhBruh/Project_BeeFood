# 📘 BeFood Big Data Project

## 🧠 Giới thiệu
Dự án **BeFood Big Data** nhằm thu thập và phân tích dữ liệu món ăn Á - Âu từ website BeFood, sử dụng hệ sinh thái Big Data gồm MongoDB, PostgreSQL, Spark và Airflow để xử lý và quản lý luồng dữ liệu.

## 🎯 Mục tiêu
- Thu thập dữ liệu món ăn từ MongoDB.
- Chuyển dữ liệu sang PostgreSQL để phân tích.
- Sử dụng Apache Spark để xử lý và phân tích dữ liệu.
- Quản lý luồng ETL qua DAG của Apache Airflow.

## 🛠️ Công nghệ & Dịch vụ sử dụng

| Dịch vụ            | Vai trò chính                                                                 |
|--------------------|-------------------------------------------------------------------------------|
| **MongoDB**        | Lưu trữ dữ liệu món ăn dạng NoSQL thu thập từ BeFood                        |
| **Mongo Express**  | Giao diện web để duyệt dữ liệu MongoDB                                      |
| **PostgreSQL**     | Lưu trữ dữ liệu dạng bảng để xử lý phân tích                                |
| **pgAdmin 4**      | Giao diện web để quản lý cơ sở dữ liệu PostgreSQL                           |
| **Apache Spark**   | Phân tích dữ liệu lớn, xử lý batch                                           |
| **Apache Airflow** | Quản lý luồng công việc ETL tự động hóa theo DAG                            |
| **Docker Compose** | Tổ chức và chạy các container đồng bộ                                        |

## 📁 Cấu trúc thư mục `befood_bigdata_dag/`

```
befood_bigdata_dag/
├── docker-compose.yml         ← Cấu hình Docker Compose cho các dịch vụ
├── dags/
│   └── befood_etl_dag.py      ← DAG ETL xử lý Mongo → Postgres → Spark
├── scripts/
│   └── spark_job.py           ← Mã xử lý dữ liệu bằng PySpark
└── tmp/                       ← Thư mục lưu file CSV tạm (export từ Mongo)
│                              
└──README.md
```

## ▶️ Hướng dẫn chạy Docker

1. **Clone hoặc tạo thư mục**
```bash
git clone https://github.com/LinhBruh/Project_BeeFood.git
cd Project_BeeFood/befood_bigdata_dag
```

2. **Chạy Docker Compose**
```bash
# Lệnh khởi động docker compose
   docker-compose up --build -d   

-- Nếu cần khởi động lại sau khi thay đổi cấu hình:
   docker-compose down
   docker-compose up -d

```

3. **Truy cập các dịch vụ**

| Dịch vụ         | Địa chỉ truy cập         | Tài khoản / Mật khẩu             |
|-----------------|--------------------------|----------------------------------|
| Mongo Express   | http://localhost:8081    | Không cần tk + mk                |
| pgAdmin 4       | http://localhost:5050    | `admin@befood.com` / `admin123`  |
| Airflow UI      | http://localhost:8088    | `airflow` / `airflow`   |
| Spark Master UI | http://localhost:8080    | Xem tiến trình Spark             |

## 🔄 Hướng dẫn kiểm thử luồng dữ liệu

1. **Tạo collection MongoDB tên `dishes`** (có thể tạo bằng Mongo Express).
2. **Bật DAG `befood_etl_dag`** trong Airflow để:
   - Trích xuất dữ liệu từ MongoDB.
   - Ghi vào PostgreSQL.
   - Gọi Spark job xử lý thống kê dữ liệu.
3. **Kiểm tra kết quả**:
   - PostgreSQL: Kiểm tra bảng `dishes` trong DB `befood_db`.
   - Spark: Output sẽ in schema, ví dụ nhóm theo `category`.

## 🔐 Thông tin kết nối nội bộ các dịch vụ

| Service      | Hostname (trong Docker network) |
|--------------|----------------------------------|
| MongoDB      | `mongo`                          |
| PostgreSQL   | `postgres`                       |
| Spark Master | `spark-master`                   |
| Airflow DAG  | `/usr/local/airflow/dags/`       |
| Spark Job    | `/usr/local/airflow/scripts/`    |

## ⚠️ Ghi chú thêm
- Lệnh chạy docker sau khi sửa
   docker-compose down
   docker-compose up -d

- Thư mục `tmp/` cần tồn tại để lưu file CSV trung gian.
- DAG có thể sửa để chạy theo `@daily`, `@hourly` hoặc thủ công tùy mục đích kiểm thử.
- Spark chạy demo đơn giản – có thể mở rộng xử lý nâng cao.
