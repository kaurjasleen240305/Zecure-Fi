const pendingLoans = [
    {
        id: 18,
        borrow_address: "0x1234567890abcdef1234567890abcdef12345678",
        loan_id: 5,
        collateral_token: "BTC",
        collateral_amount_can_pay: 0.01,
        deadline_can_repay: "2025-05-15",
        has_passed_threshold: true,
        isApproved: true,
        status: "Not Paid"
    },
    {
        id: 25,
        borrow_address: "0x1234567890abcdef1234567890abcdef12345678",
        loan_id: 12,
        collateral_token: "MATIC",
        collateral_amount_can_pay: 100,
        deadline_can_repay: "2025-04-25",
        has_passed_threshold: false,
        isApproved: true,
        status: "Not Paid"
    },
    {
        id: 17,
        borrow_address: "0x1234567890abcdef1234567890abcdef12345678",
        loan_id: 18,
        collateral_token: "DAI",
        collateral_amount_can_pay: 2800,
        deadline_can_repay: "2025-08-15",
        has_passed_threshold: true,
        isApproved: true,
        status: "Not Paid"
    },
    {
        id: 18,
        borrow_address: "0x1234567890abcdef1234567890abcdef12345678",
        loan_id: 16,
        collateral_token: "ETH",
        collateral_amount_can_pay: 0.7,
        deadline_can_repay: "2025-05-20",
        has_passed_threshold: false,
        isApproved: true,
        status: "Not Paid"
    },
    {
        id: 98,
        borrow_address: "0x1234567890abcdef1234567890abcdef12345678",
        loan_id: 27,
        collateral_token: "MATIC",
        collateral_amount_can_pay: 90,
        deadline_can_repay: "2025-07-05",
        has_passed_threshold: false,
        isApproved: true,
        status: "Not Paid"
    }
];

module.exports = pendingLoans;