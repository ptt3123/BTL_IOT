        let currentPage = 1;
        let totalItems = 0;
        let pageSize = 20;
        let totalPages = 0;
        let txt = "";

        // Hàm cập nhật phân trang
        function updatePagination() {
            const prevButton = document.getElementById("prevPage");
            const nextButton = document.getElementById("nextPage");
            const currentPageElement = document.getElementById("currentPage");
            const totalPagesElement = document.getElementById("totalPages");

            // Cập nhật số trang hiện tại
            currentPageElement.textContent = currentPage;
            totalPagesElement.textContent = totalPages;

            prevButton.classList.toggle("disabled", currentPage <= 1);
            nextButton.classList.toggle("disabled", currentPage >= totalPages);
        }

        // Hàm thay đổi trang
        function changePage(delta) {
            currentPage += delta;
            if (currentPage < 1) currentPage = 1;
            if (currentPage > totalPages) currentPage = totalPages;

            fetchData();
        }

        // Gọi API để lấy dữ liệu và cập nhật bảng
        async function fetchData() {
            txt = document.getElementById("txt").value;
            pageSize = document.querySelector('input[name="pagesize"]').value;
            const sortOrder = document.getElementById('sortOrder').value;
            const sortItem = document.getElementById('sortItem').value;
            const response = await fetch(`/api/database?txt=${txt}&pagesize=${pageSize}&page=${currentPage}&item=${sortItem}&order=${sortOrder}`);
            const result = await response.json();

            totalItems = result.total;
            totalPages = Math.ceil(totalItems / pageSize);
            updateTable(result.data);
            updatePagination();
        }

        // Cập nhật bảng với dữ liệu mới
        function updateTable(data) {
            const tableBody = document.querySelector("#dataTable tbody");
            tableBody.innerHTML = ""; // Xóa bảng hiện tại

            data.forEach(item => {
                const row = document.createElement("tr");
                const cellId = document.createElement("td");
                const cellTem = document.createElement("td");
                const cellHum = document.createElement("td");
                const cellLig = document.createElement("td");
                const cellTim = document.createElement("td");

                cellId.textContent = item.id;
                cellTem.textContent = item.tem;
                cellHum.textContent = item.hum;
                cellLig.textContent = item.lig;
                cellTim.textContent = item.tim;

                row.appendChild(cellId);
                row.appendChild(cellTem);
                row.appendChild(cellHum);
                row.appendChild(cellLig);
                row.appendChild(cellTim);

                tableBody.appendChild(row);
            });
        }

        // Xử lý sự kiện submit form tìm kiếm
        document.getElementById("searchForm").addEventListener("submit", (event) => {
            event.preventDefault();
            currentPage = 1;
            fetchData();
        });

        // Khởi tạo phân trang khi tải trang
        window.onload = function() {
            fetchData();
        };

        // Sự kiện cho phân trang
        document.getElementById("prevPage").addEventListener("click", () => changePage(-1));
        document.getElementById("nextPage").addEventListener("click", () => changePage(1));