const active_loans = [
    {
        id: 1,
        lender_address: "0xAbCdEf1234567890abcdef1234567890AbCdEf12",
        credit_score_threshold: 700,
        lending_token: "DAI",
        lending_amount: 1000,
        collateral_token: "ETH",
        minimum_collateral_amount: 0.5,
        deadline_repaying: "2025-06-01",
        is_Active_Loan: true
    },
    {
        id: 3,
        lender_address: "0xCDA123456789abcdef9876543210abcdef987654",
        credit_score_threshold: 720,
        lending_token: "USDC",
        lending_amount: 2000,
        collateral_token: "ETH",
        minimum_collateral_amount: 1,
        deadline_repaying: "2025-07-10",
        is_Active_Loan: true
    },
    {
        id: 5,
        lender_address: "0xEfA9876543210abcdef9876543210abcdef987654",
        credit_score_threshold: 680,
        lending_token: "WBTC",
        lending_amount: 0.05,
        collateral_token: "ETH",
        minimum_collateral_amount: 0.3,
        deadline_repaying: "2025-06-30",
        is_Active_Loan: true
    },
    {
        id: 6,
        lender_address: "0xFA9876543210abcdef1234567890abcdef1234567",
        credit_score_threshold: 750,
        lending_token: "USDT",
        lending_amount: 3000,
        collateral_token: "DAI",
        minimum_collateral_amount: 2800,
        deadline_repaying: "2025-08-15",
        is_Active_Loan: true
    },
    {
        id: 8,
        lender_address: "0x2B34567890abcdef1234567890abcdef123456789",
        credit_score_threshold: 700,
        lending_token: "DAI",
        lending_amount: 5000,
        collateral_token: "BTC",
        minimum_collateral_amount: 0.08,
        deadline_repaying: "2025-09-10",
        is_Active_Loan: true
    },
    {
        id: 9,
        lender_address: "0x3C4567890abcdef9876543210abcdef9876543210",
        credit_score_threshold: 690,
        lending_token: "USDC",
        lending_amount: 1500,
        collateral_token: "MATIC",
        minimum_collateral_amount: 90,
        deadline_repaying: "2025-07-05",
        is_Active_Loan: true
    },
    {
        id: 11,
        lender_address: "0x5E67890abcdef1234567890abcdef1234567890ab",
        credit_score_threshold: 670,
        lending_token: "DAI",
        lending_amount: 1200,
        collateral_token: "ETH",
        minimum_collateral_amount: 0.6,
        deadline_repaying: "2025-06-20",
        is_Active_Loan: true
    },
    {
        id: 12,
        lender_address: "0x6F7890abcdef1234567890abcdef1234567890abcd",
        credit_score_threshold: 710,
        lending_token: "USDC",
        lending_amount: 2200,
        collateral_token: "BTC",
        minimum_collateral_amount: 0.05,
        deadline_repaying: "2025-07-15",
        is_Active_Loan: true
    }
]

module.exports = active_loans;