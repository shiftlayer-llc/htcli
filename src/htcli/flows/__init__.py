"""
Hypertensor CLI Automated Flows

This module provides automated workflows that combine multiple CLI operations
into streamlined, user-friendly processes with minimal human intervention.
"""

from .development_setup import DevelopmentSetupFlow
from .migration_recovery import MigrationRecoveryFlow
from .node_onboarding import NodeOnboardingFlow
from .staking_portfolio import StakingPortfolioFlow
from .subnet_deployment import SubnetDeploymentFlow

__all__ = [
    "SubnetDeploymentFlow",
    "NodeOnboardingFlow",
    "StakingPortfolioFlow",
    "DevelopmentSetupFlow",
    "MigrationRecoveryFlow",
]

# Flow registry for dynamic access
AVAILABLE_FLOWS = {
    "subnet-deployment": SubnetDeploymentFlow,
    "node-onboarding": NodeOnboardingFlow,
    "staking-portfolio": StakingPortfolioFlow,
    "development-setup": DevelopmentSetupFlow,
    "migration-recovery": MigrationRecoveryFlow,
}
