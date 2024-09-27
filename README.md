# Overview

This document provides a comprehensive overview of the architecture, approach, and integration plan for incorporating post-quantum cryptographic (PQC) functions into a blockchain system. The main objective is to ensure the long-term security of blockchain networks by making them resistant to potential attacks from quantum computers, which could, in the future, compromise widely-used cryptographic algorithms such as RSA and ECC (Elliptic Curve Cryptography).

## 1.1 Motivation

As advancements in quantum mechanics continue, our understanding of subatomic particles has led to the creation of increasingly powerful quantum computers. If a sufficiently powerful quantum computer is developed, it could run Shor's algorithm—an algorithm designed to factor large prime numbers. Current cryptographic algorithms for private and public key generation, digital signatures, and verification rely on the computational difficulty of factoring the product of two primes. If such a machine becomes a reality, it could break most asymmetric public key encryption systems in use today. Therefore, transitioning to post-quantum cryptographic algorithms is critical to securing blockchain technologies.

## 1.2 Objectives

- Enable secure, quantum-resistant blockchain transactions.
- Upgrade cryptographic algorithms for digital signatures and key exchanges to quantum-resistant versions.
- Maintain compatibility with existing cryptographic algorithms during the transition phase, avoiding the need for a hard fork.

## Architectural Components

Integrating PQC into blockchain will affect several core components. This section outlines the key elements of the architecture:

### Key Generation

The process for generating public and private keys will be updated so that all new wallets use post-quantum cryptographic key pairs. This ensures that the number of users relying on pre-quantum keys will, at worst, remain constant while additional measures are taken to facilitate a smooth transition.

### Signing & Verification

The signing and verification mechanisms will adopt a hybrid approach, employing different signing functions based on the type of key in use. This ensures backward compatibility with legacy wallets while enhancing blockchain security. To illustrate, we’ve developed a single relay server that supports both pre-quantum and post-quantum clients. The server executes distinct functions depending on the client in use.

### Storage

Post-quantum keys will be stored in a separate database from pre-quantum keys due to their larger size. This decision was driven by the need for resource efficiency. Storing both types of keys in the same database would require fields large enough to accommodate post-quantum keys, which are approximately 60 to 70 times larger than pre-quantum keys, making this approach inefficient.

## Approach

Rather than migrating all cryptographic functions from pre-quantum to post-quantum algorithms, we have selectively strengthened vulnerable points in the system. Post-quantum algorithms are computationally intensive, and fully transitioning to them could result in significant performance degradation. Since blockchains need to handle high transaction volumes while maintaining resilience, a substantial slowdown would render them impractical for many use cases. Therefore, a hybrid approach, combining both pre-quantum and post-quantum algorithms, is optimal. This strategy secures high-risk areas while minimizing performance impacts.

## Implementation



This is a relay server designed to facilitate communication between nodes. Ideally, nodes would connect directly to each other, forming a peer-to-peer network. However, due to network challenges—such as node discovery and locating a node’s public-facing IP address—we’ve opted to connect the nodes via a relay server. 

The server acts as a central point for broadcasting new transactions, blocks, and wallet addresses to other nodes. While this implementation is not fully decentralized, it is sufficient for the proof of concept we aim to build.

### Running the Server Locally

To run this server on your local machine, follow these steps:

1. **Clone the Repository:**
   Clone the repository using the following command:

   ```bash
   git clone https://github.com/kdukuray/Qoin-Relay-Server/tree/master
   ```

2. **Install Dependencies:**
   Install all the required dependencies from the `requirements.txt` file by running:

   ```bash
   pip install -r requirements.txt
   ```

3. **Migrate the Database:**
   This is a Django server, so you will need to create the necessary database migrations and apply them:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a Superuser:**
   To access the admin panel, create a superuser with the following command:

   ```bash
   python manage.py createsuperuser
   ```

5. **Create a Genesis Block:**
   Log into the admin panel and create a genesis block. Set both the `block_hash` and `prev_block_hash` to "GenesisBlock".

6. **Start the Server:**
   After the setup is complete, navigate to the project directory and run the following command to start the server:

   ```bash
   python manage.py runserver
   ```

### Important Note:

If you encounter issues with the `pqcrypto` library, it may be due to missing compiled C bindings for some of the cryptographic functions. To resolve this, navigate to the `site-packages` folder within your virtual environment and run:

```bash
sudo python3 compile.py
```

This should resolve any compilation issues.
