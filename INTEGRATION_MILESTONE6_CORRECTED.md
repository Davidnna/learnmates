# LearnMeets AI — Corrected Milestone 6: Account Management Across Both Interfaces

## Why this correction exists
Milestone 5 added account management to the React frontend and its API, but the legacy Flask-rendered interface did not include the account page. If the deployed/local app was serving Flask templates, the visible changes would therefore not appear. This corrected package adds the account-management page and navigation link to the Flask interface as well, while retaining the React implementation.

## Included
- Removed the inactive notification control from the React workspace top bar (the React top bar now uses account/settings navigation instead).
- React `/account` page for display-name updates and password changes.
- Flask `/account` page with display-name editing and password changes.
- Account-management navigation link in the Flask template navbar.
- Password changes verify the current password and require a new password of at least eight characters.
- Both interfaces reuse the existing user table and database; no reset or schema migration is required.

## Not included yet
- Profile photo uploads: require persistent object storage and upload validation.
- Google sign-in: requires OAuth credentials, callback URLs, and account-linking/security configuration.
- Email-address changes.

## Validation performed
- Python syntax compilation of `app.py` passed.
- ZIP integrity check passed.
- Flask template runtime and React production build still need to be tested in the project's configured environment before deployment.

## Manual test plan
1. Start the Flask app, sign in, and verify Account management appears in the navigation.
2. Open `/account`, update the display name, and verify it persists after refresh.
3. Attempt password change with an incorrect current password and confirm rejection.
4. Change the password with the correct current password and verify the new password works after sign-in.
5. Start the React frontend, open `/account`, and repeat profile/password tests through the API.
6. Confirm no notification bell is displayed in the React workspace header.

## Git commit message
`fix: expose account management in Flask and React interfaces`

Suggested command:
`git add app.py templates/base.html templates/account.html frontend INTEGRATION_MILESTONE6_CORRECTED.md && git commit -m "fix: expose account management in Flask and React interfaces"`
