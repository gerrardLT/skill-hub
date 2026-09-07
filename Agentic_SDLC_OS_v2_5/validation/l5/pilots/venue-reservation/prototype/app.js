const reserveButton = document.querySelector('#reserveButton');
const resetButton = document.querySelector('#resetButton');
const activity = document.querySelector('#activity');
const statusBadge = document.querySelector('#statusBadge');
const availableCount = document.querySelector('#availableCount');
const queueCount = document.querySelector('#queueCount');
const toast = document.querySelector('#toast');
let step = 0;

function showToast(message) {
  toast.textContent = message;
  toast.hidden = false;
  window.setTimeout(() => { toast.hidden = true; }, 2200);
}

function setActivity(kind, mark, title, copy) {
  activity.className = `activity ${kind}`;
  activity.innerHTML = `<div class="activity-mark" aria-hidden="true">${mark}</div><div><strong>${title}</strong><p>${copy}</p></div>`;
}

reserveButton.addEventListener('click', async () => {
  reserveButton.disabled = true;
  reserveButton.textContent = '服务端确认中…';
  setActivity('pending', '…', '正在校验容量', '请求使用幂等键提交；成功状态仅由服务端响应决定。');
  await new Promise(resolve => window.setTimeout(resolve, 650));

  if (step === 0) {
    availableCount.textContent = '0';
    statusBadge.textContent = '已满 · 可候补';
    statusBadge.className = 'status waitlist';
    setActivity('reserved', '✓', '预约成功', '已锁定 19:00 场次。订单号：RSV-DEMO-001。');
    reserveButton.textContent = '演示下一位会员';
    showToast('预约成功，容量已原子扣减。');
  } else if (step === 1) {
    queueCount.textContent = '1 人';
    setActivity('waitlisted', '1', '候补成功 · 第 1 位', '名额释放后按 FIFO 自动转正，并通过通知触达。');
    reserveButton.textContent = '演示取消并转正';
    showToast('场次已满，已进入候补队列。');
  } else {
    queueCount.textContent = '0 人';
    setActivity('reserved', '↑', '候补已自动转正', '原预约取消后，队首会员在同一事务中获得名额。');
    reserveButton.textContent = '闭环已完成';
    reserveButton.disabled = true;
    showToast('FIFO 转正完成，无超售。');
    step += 1;
    return;
  }
  step += 1;
  reserveButton.disabled = false;
});

resetButton.addEventListener('click', () => {
  step = 0;
  availableCount.textContent = '1';
  queueCount.textContent = '0 人';
  statusBadge.textContent = '尚有名额';
  statusBadge.className = 'status available';
  reserveButton.disabled = false;
  reserveButton.textContent = '确认预约 · ¥68';
  setActivity('empty', '○', '尚未提交', '点击预约后查看成功、候补及自动转正状态。');
  showToast('演示已重置。');
});
