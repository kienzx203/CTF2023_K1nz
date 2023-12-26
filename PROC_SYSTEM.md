# **/proc Filesystem**

- Hệ thống tệp Proc hoạt động như một giao diện cho các cấu trúc dữ liệu nội bộ trong kernel. Nó có thể được sử dụng để lấy thông tin về hệ thống và thay đổi các tham số kernel nhất định khi chạy `(sysctl)`.

## **Process-Specific Subdirectories (Thư mục con dành riêng cho quy trình)**

- Thư mục /proc chứa (trong số những thứ khác) một thư mục con cho mỗi tiến trình đang chạy trên hệ thống, được đặt tên theo ID tiến trình (PID).

![](./img_proc/Screenshot%202023-08-29%20163910.png)

| File    | Content |
| ----------- | ----------- |
| clear_refs | Clears page referenced bits shown in smaps output   (Xóa các bit tham chiếu trang được hiển thị trong đầu ra smaps)  |
| cmdline |Command line arguments (Đối số dòng lệnh)|
|cpu| Current and last cpu in which it was executed (2.4)(smp)  (CPU hiện tại và cuối cùng mà nó được thực thi (2.4)(smp)) |
|cwd|Link to the current working directory (Liên kết đến thư mục làm việc hiện tại)|
|environ|Values of environment variables (Giá trị của biến môi trường)|
|exe|Link to the executable of this process (Liên kết tới tệp thực thi của quy trình này)|
|fd|Directory, which contains all file descriptors (Thư mục chứa tất cả các bộ mô tả tập tin) |
|maps|Memory maps to executables and library files (2.4) (Ánh xạ bộ nhớ tới các tệp thực thi và tệp thư viện (2.4))|
|mem|Memory held by this process (Bộ nhớ được giữ bởi quá trình này)|
|root|Link to the root directory of this process (Liên kết đến thư mục root của quá trình này)|
|stat|Process status (Trạng thái đang tiến trình diễn ra)|
|statm|Process memory status information (Xử lý thông tin trạng thái bộ nhớ)|
|status|Process status in human readable form (Trạng thái quy trình ở dạng con người có thể đọc được)|
|wchan| Present with CONFIG_KALLSYMS=y: it shows the kernel function symbol the task is blocked in - or "0" if not blocked. (Trình bày với CONFIG_KALLSYMS=y: nó hiển thị ký hiệu hàm kernel mà tác vụ bị chặn - hoặc "0" nếu không bị chặn.)|
|pagemap|Page table|
|stack|Report full stack trace, enable via CONFIG_STACKTRACE (Báo cáo dấu vết ngăn xếp đầy đủ, kích hoạt qua CONFIG_STACKTRACE)|
|smaps| An extension based on maps, showing the memory consumption of each mapping and flags associated with it (Tiện ích mở rộng dựa trên bản đồ, hiển thị mức tiêu thụ bộ nhớ của từng ánh xạ và các cờ được liên kết với nó) |
|smaps_rollup|Accumulated smaps stats for all mappings of the process. This can be derived from smaps, but is faster and more convenient (Số liệu thống kê về bản đồ tích lũy cho tất cả các bản đồ của quy trình. Điều này có thể bắt nguồn từ smap, nhưng nhanh hơn và thuận tiện hơn)|
|numa_maps|	An extension based on maps, showing the memory locality and binding policy as well as mem usage (in pages) of each mapping. (Tiện ích mở rộng dựa trên bản đồ, hiển thị vị trí bộ nhớ và chính sách ràng buộc cũng như mức sử dụng mem (tính bằng trang) của mỗi ánh xạ.)|