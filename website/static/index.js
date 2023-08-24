function deleteGroup(groupId) {
  fetch("/delete-group", {
    method: "POST",
    body: JSON.stringify({ groupId: groupId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


function deleteExpense(expenseId, groupId) {
  fetch("/delete-expense", {
    method: "POST",
    body: JSON.stringify({ expenseId: expenseId }),
  }).then((_res) => {
    window.location.href = `/group-view-${groupId}`;
  });
}

function deleteUserDebts(memberId, groupId, member_twoId, amount) {
  fetch("/delete-user-debt", {
    method: "POST",
    body: JSON.stringify({ MemberId: memberId, Member_twoId: member_twoId, Amount: amount, GroupId: groupId}),
  }).then((_res) => {
    window.location.href = `/group-view-${groupId}`;
  });
}