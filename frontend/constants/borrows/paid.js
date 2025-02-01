const paidLoans = [
    {
        id: 12,
        borrow_address: "0x1234567890abcdef1234567890abcdef12345678",
        loan_id: 3,
        collateral_token: "ETH",
        collateral_amount_can_pay: 0.5,
        deadline_can_repay: "2025-06-01",
        has_passed_threshold: true,
        isApproved: true,
        status: "Paid"
    },
    {
        id: 20,
        borrow_address: "0x1234567890abcdef1234567890abcdef12345678",
        loan_id: 4,
        collateral_token: "ETH",
        collateral_amount_can_pay: 1,
        deadline_can_repay: "2025-07-10",
        has_passed_threshold: true,
        isApproved: true,
        status: "Paid"
    },
    {
        id: 16,
        borrow_address: "0x1234567890abcdef1234567890abcdef12345678",
        loan_id: 19,
        collateral_token: "ETH",
        collateral_amount_can_pay: 0.3,
        deadline_can_repay: "2025-06-30",
        has_passed_threshold: true,
        isApproved: true,
        status: "Paid"
    },
    {
        id: 23,
        borrow_address: "0x1234567890abcdef1234567890abcdef12345678",
        loan_id: 13,
        collateral_token: "BTC",
        collateral_amount_can_pay: 0.08,
        deadline_can_repay: "2025-09-10",
        has_passed_threshold: true,
        isApproved: true,
        status: "Paid"
    },
    {
        id: 100,
        borrow_address: "0x1234567890abcdef1234567890abcdef12345678",
        loan_id: 34,
        collateral_token: "DAI",
        collateral_amount_can_pay: 1800,
        deadline_can_repay: "2025-06-12",
        has_passed_threshold: true,
        isApproved: true,
        status: "Paid"
    }
];

module.exports=paidLoans