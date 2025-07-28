# Drop Me Recycling Backend API

#Task1_Intern

## Overview

This backend API supports **Drop Me**, a recycling rewards platform where users earn points by depositing recyclable materials through smart machines located at various places.

---

## Models & Business Logic

### User

- Extended Django’s user model with extra fields:
  - **Address**: Tracks where users use machines to identify active locations and plan expansions.
  - **Age & Gender**: Helps understand the target audience using the machines.
  - **Unique username and email**: Required for secure login.
  - **Minimal required fields for signup**: Only email, username, and password, to keep registration fast and simple.

- Email OTP verification via Django’s email system ensures users are verified before receiving sensitive info like reward summaries by email.

---

### Deposit

- Represents each recycling deposit by a user.
- Tracks **material type** (plastic, metal, glass) and **weight (kg)**.
- Automatically calculates **reward points** based on material:
  - Plastic = 1 point/kg
  - Glass = 2 points/kg
  - Metal = 3 points/kg

---

### Redemption

- Allows admins (e.g., supermarket staff) to **redeem points** on users’ behalf.
- Admins can deduct some or all points during redemption.
- Ensures users cannot redeem more points than they have.

---

## API Endpoints & Usage

The API is split into two main apps, with base URLs:

---

### Accounts (User Management & Auth)

- POST /accounts/register/ — Register new users quickly with username, email, and password.

- POST /accounts/login/ — Login to get JWT tokens.

- POST /accounts/logout/ — Logout endpoint.

- POST /accounts/send-email-otp/ — Send verification OTP to user email.

- POST /accounts/verify-email-otp/ — Verify OTP to activate account.

- POST /accounts/refresh/ — Refresh JWT token.

---

### Deposits & Rewards

- POST /deposits/deposit/ — Submit a new deposit (authenticated users only). Reward points auto-calculated.

- GET /deposits/summary/ — Get user’s total recycled weight, total points, used points, and remaining points.

- POST /deposits/send-email-summary/ — Send email summary to verified users only.

- POST /deposits/deduct-points/ — Admin endpoint to deduct points from user during redemption.

---

### Workflow Summary

- User signs up quickly with essential info.

- User verifies their email via OTP for security.

- User deposits recyclables at machines tracked by address.

- System calculates points based on material and weight.

- User checks their points and weights anytime via API.

- Admins redeem points on users’ behalf.

- Verified users can request email summaries of their recycling stats.

---

### Notes

- Phone verification is not implemented due to lack of free SMS APIs; email OTP covers verification securely.

- Security is key: Only verified users get email summaries.

- The system is built for simplicity, maintainability, and future extensibility.
