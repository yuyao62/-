let inventoryData = [];
let chartInstance = null;

fetch("中國_盤點結果_20251211_121418.json")
  .then(response => response.json())
  .then(data => {
    inventoryData = data;
    populateVendorOptions();
    searchDrug();
  })
  .catch(error => console.error("載入 JSON 失敗:", error));

function populateVendorOptions() {
  const vendorSet = new Set();
  inventoryData.forEach(item => {
    const vendor = item["廠商"] || item["vendor"];
    if (vendor) vendorSet.add(vendor);
  });

  const vendorSelect = document.getElementById("vendorSelect");
  vendorSet.forEach(vendor => {
    const option = document.createElement("option");
    option.value = vendor;
    option.textContent = vendor;
    vendorSelect.appendChild(option);
  });
}

function searchDrug() {
  const keyword = document.getElementById("searchInput").value.trim();
  const selectedVendor = document.getElementById("vendorSelect").value;
  const outOfStockOnly = document.getElementById("outOfStockFilter").checked;
  const tbody = document.querySelector("#resultTable tbody");
  tbody.innerHTML = "";

  const results = inventoryData.filter(item => {
    const code = item["藥品代碼"] || item["code"] || "";
    const name = item["藥品名稱"] || item["name"] || "";
    const vendor = item["廠商"] || item["vendor"] || "";
    const qty = item["盤點數量"] || item["qty"] || 0;

    const matchVendor = selectedVendor ? vendor === selectedVendor : true;
    const matchKeyword = code.includes(keyword) || name.includes(keyword);
    const stockFilter = outOfStockOnly ? qty === 0 : true;

    return matchVendor && matchKeyword && stockFilter;
  });

  results.forEach(item => {
    const vendor = item["廠商"] || item["vendor"] || "";
    const code = item["藥品代碼"] || item["code"] || "";
    const name = item["藥品名稱"] || item["name"] || "";
    const qty = item["盤點數量"] || item["qty"] || 0;

    const row = `<tr>
      <td>${vendor}</td>
      <td>${code}</td>
      <td>${name}</td>
      <td>${qty}</td>
      <td>${qty === 0 ? "缺貨" : "有庫存"}</td>
    </tr>`;
    tbody.innerHTML += row;
  });

  updateStats(results);
}

function resetSearch() {
  document.getElementById("searchInput").value = "";
  document.getElementById("vendorSelect").value = "";
  document.getElementById("outOfStockFilter").checked = false;
  searchDrug();
}

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

function drawChart(total, outOfStock) {
  const ctx = document.getElementById("chart").getContext("2d");

  if (chartInstance) chartInstance.destroy();

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
        legend: { position: "bottom" },
        title: { display: true, text: "缺貨比例" }
      }
    }
  });
}
