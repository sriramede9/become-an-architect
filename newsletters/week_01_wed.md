# ⚡ Week 1: Temporary Access Delegation & STS Mechanics

## 🎯 Curiosity Trigger
How do you grant an application ephemeral permission to perform high-privilege actions without ever exposing long-term credentials? The answer lies in the transition from identity-based security to dynamic, time-bound tokenization.

## 🏰 The Springfield Chronicles
Imagine Mr. Burns is locked deep within his reinforced, lead-lined security vault, completely inaccessible to the outside world. Yet, the Springfield Nuclear Power Plant continues to receive high-stakes, classified shipments of radioactive isotopes. Waylon Smithers, acting as the trusted intermediary, cannot simply use Mr. Burns' personal biometric keys—those are locked inside the vault.

Instead, Smithers carries a "Power of Attorney" document (the **IAM Role**). When a delivery arrives, Smithers presents this document to the plant’s security guard (the **AWS Security Token Service - STS**). The guard verifies the document's authenticity against the master registry (the **Trust Policy**). Upon validation, the guard issues Smithers a temporary, one-time badge (the **STS Session Token**) that allows him to sign for that specific delivery. Once the delivery is signed, the badge expires, and Smithers’ authority vanishes. Even if a thief mugged Smithers five minutes later, the badge would be useless, as the authorization was strictly bound to that specific transaction and time window.

## 🛠️ Technical Concept Deep-Dive
*   **IAM Roles:** An identity with no long-term credentials (no AKIA/Secret Key). It is defined by two policies:
    *   **Trust Policy (Resource-based):** Defines *who* (principal) is allowed to `sts:AssumeRole`.
    *   **Permissions Policy (Identity-based):** Defines *what* the role is allowed to do once assumed.
*   **AWS STS (Security Token Service):** The engine of delegation. It issues temporary credentials consisting of an `AccessKeyId`, `SecretAccessKey`, and a `SessionToken`.
*   **IMDSv2 (Instance Metadata Service):** The critical delivery mechanism for EC2. By enforcing `HttpTokens: required` (PUT requests), we mitigate SSRF vulnerabilities that could otherwise be used to exfiltrate tokens.

## 🧬 Architectural Design Evolution
*   **The Monorail Anti-Pattern (Worst):** Hardcoding IAM User Access Keys in `git` commits. This is a "set it and forget it" disaster that creates an infinite blast radius if the repository is leaked.
*   **The Industrial Patch (Moderate):** Storing credentials in `.env` files. While out of version control, it requires manual rotation via SSH/scripts. It is fragile, prone to human error, and lacks auditability.
*   **The Well-Architected Masterpiece (Best):** Attaching an IAM Role to an EC2 Instance Profile. The application uses the AWS SDK to query `http://169.254.169.254/latest/meta-data/iam/security-credentials/`. The SDK automatically handles the rotation of tokens before they expire, ensuring zero-touch credential management.

## 🚧 Architectural Guardrails: Do's and Don'ts
*   **Do:** Use the Principle of Least Privilege (PoLP) when defining role permissions.
*   **Do:** Enable CloudTrail to monitor `AssumeRole` events.
*   **Don't:** Use `AssumeRole` for human users; use IAM Identity Center (SSO) instead.
*   **Don't:** Set session durations longer than necessary for the task at hand.

## 🔍 Similar Problems to Study
*   **Cross-Account Access:** Assuming roles across different AWS accounts.
*   **OIDC Federation:** How GitHub Actions assumes roles to deploy infrastructure without long-term keys.
*   **ABAC (Attribute-Based Access Control):** Using session tags to dynamically limit role permissions.

## 🏗️ Weekend Micro-Project Blueprint
1.  **Create a Role:** Create an IAM role with `AmazonS3ReadOnlyAccess`.
2.  **Trust Policy:** Set the Trust Policy to allow `ec2.amazonaws.com` to assume the role.
3.  **Launch EC2:** Launch an instance and attach the role via an Instance Profile.
4.  **Verification:** SSH into the instance and run `aws s3 ls`. Observe that no credentials are configured in `~/.aws/credentials`.
5.  **Force IMDSv2:** Modify the instance metadata settings to require IMDSv2 and test that the SDK still functions correctly.

## 📐 Technical Calculations & Logic
The session validity window is governed by the `DurationSeconds` parameter in the `AssumeRole` API call. The relationship between the token expiration and the architectural constraints is defined as:

$$T_{exp} = T_{start} + \text{DurationSeconds}$$

Where the effective window for an authentication chain must satisfy:

$$\forall \text{ operations } o \in O, \text{ time}(o) < T_{exp}$$

For EC2 Instance Profiles, the default duration is 1 hour, but the SDK performs a background refresh when the remaining time $T_{rem}$ falls below a threshold $\tau$:

$$\tau \approx \frac{1}{6} \text{DurationSeconds}$$

## 🌪️ The Architect's Cliffhanger
If an EC2 instance is compromised via a high-severity Remote Code Execution (RCE) vulnerability, the attacker can use the Instance Profile to assume the role. If the role has `AdministratorAccess`, the entire account is compromised. **Is it safer to have one "God-mode" role attached to the instance, or to architect a system where the application must perform a secondary MFA-backed `AssumeRole` call to elevate privileges for specific, sensitive administrative tasks?**