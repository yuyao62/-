// 盤點查詢器 app.js

let inventoryData = [];

// 載入 JSON 檔案（由 excel_to_json.py 轉換而來）
fetch("中國_盤點結果_20251211_121418.json")
  .then(response => response.json())
  .then(data => {
    inventoryData = data;
    console.log("資料載入完成", inventoryData);
    searchDrug(); // 初始顯示
  })
  .catch(error => console.error("載入 JSON 失敗:", error));

// 查詢藥品
function searchDrug() {
  const keyword = document.getElementById("searchInput").value.trim();
  const outOfStockOnly = document.getElementById("outOfStockFilter").checked;
  const tbody = document.querySelector("#resultTable tbody");
  tbody.innerHTML = "";

  const results = inventoryData.filter(item => {
    // 偵測欄位名稱（可能是中文或英文）
    const code = item["藥品代碼"] || item["code"] || "";
    const name = item["藥品名稱"] || item["name"] || "";
    const qty = item["盤點數量"] || item["qty"] || 0;

    const match = code.includes(keyword) || name.includes(keyword);
    const stockFilter = outOfStockOnly ? qty === 0 : true;
    return match && stockFilter;
  });

  results.forEach(item => {
    const code = item["藥品代碼"] || item["code"] || "";
    const name = item["藥品名稱"] || item["name"] || "";
    const qty = item["盤點數量"] || item["qty"] || 0;

    const row = `<tr>
      <td>${code}</td>
      <td>${name}</td>
      <td>${qty}</td>
      <td>${qty === 0 ? "缺貨" : "有庫存"}</td>
    </tr>`;
    tbody.innerHTML += row;
  });

  updateStats(results);
}

// 重置查詢
function resetSearch() {
  document.getElementById("searchInput").value = "";
  document.getElementById("outOfStockFilter").checked = false;
  searchDrug();
}

// 更新統計摘要
function updateStats(results) {
  const total = results.length;
  const outOfStock = results.filter(item => {
    const qty = item["盤點數量"] || item["qty"] || 0;
    return qty === 0;
  }).length;
  const rate = total > 0 ? Math.round((outOfStock / total) * 100) : 0;

  document.getElementById("totalCount").textContent = total;
  document.getElementById("outOfStockCount").textContent = outOfStock;
  document.getElementById("outOfStockRate").textContent = rate + "%";

  drawChart(total, outOfStock);
}

// 繪製 Chart.js 圖表
let chartInstance = null;
function drawChart(total, outOfStock) {
  const ctx = document.getElementById("chart").getContext("2d");

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["有庫存", "缺貨"],
      datasets: [{
        data: [total - outOfStock, outOfStock],
        backgroundColor: ["#2ecc71", "#e74c3c"]
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom"
        },
        title: {
          display: true,
          text: "缺貨比例"
        }
      }
    }
  });
}
