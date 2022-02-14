const pinCodeTag = document.querySelector(".pincode");
const areaTag = document.querySelector(".area");
const districtTag = document.querySelector(".district");
const stateTag = document.querySelector(".state");

async function apiFetcher(pincode) {
  let url = `https://api.postalpincode.in/pincode/${pincode}`;
  let data = await fetch(url);
  data = await data.json();
  return data;
}

pinCodeTag.addEventListener("input", async () => {
  if (pinCodeTag.value.length === 6) {
    let area = ``;
    let data = await apiFetcher(pinCodeTag.value);
    console.log(data);
    data = await data[0];
    if (data.Status === "Success") {
      await data.PostOffice.forEach((e) => {
        area += ` <option value="${e.Name}" selected class="form--input-value">${e.Name}</option>`;
      });
      districtTag.value = data.PostOffice[0].District;
      stateTag.value = data.PostOffice[0].State;
      areaTag.innerHTML = await area;
    } else {
      areaTag.innerHTML = ` <option value=${null} selected disableled class="form--input-value">Sorry No area found</option>`;
      districtTag.value = "No District found";
      stateTag.value = "No State found";
    }
  } else {
    areaTag.innerHTML = ` <option value=${null} selected disableled class="form--input-value">Sorry No area found</option>`;
    districtTag.value = "No District found";
    stateTag.value = "No State found";
  }
});
