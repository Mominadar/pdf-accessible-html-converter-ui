import hre  from "hardhat";

async function deployContract(contractName){
  const contractFactory = await hre.ethers.getContractFactory(contractName);  
  const registry = await contractFactory.deploy();
  // Wait for deployment to complete
  await registry.waitForDeployment();
  // Get deployed contract address
  const contractAddress = await registry.getAddress();
  console.log(`Contract deployed at: ${contractAddress}`);
}

async function main() {
  await deployContract("DIDRegistry");
  await deployContract("BirthCertificateRegistry");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

