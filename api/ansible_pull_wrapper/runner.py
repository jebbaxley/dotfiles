""""""""""""""""""""ansible_pull_wrapper.runner

Small, focused wrapper around the `ansible-pull` command that:
- constructs a safe argument list (no shell=True)
- validates the presence of ansible-pull
- runs the command with subprocess and returns the CompletedProcess
- provides a dry-run mode for testing

Design goals:
- DRY and single-responsibility: build_ansible_pull_cmd builds the CLI args,
  run_ansible_pull executes them.
- Readable and documented: each function has a docstring and explanatory comments.
- High-performance: minimal overhead; uses subprocess.run with list args.
- Library-friendly: small public API, type-hinted, explicit exceptions.
""""""""""""""""""""from __future__ import annotations

import logging
import shutil
import subprocess
from typing import List, Optional

logger = logging.getLogger(__name__)

# Public API
__all__ = ["build_ansible_pull_cmd", "run_ansible_pull", "AnsiblePullError"]


class AnsiblePullError(RuntimeError):
    """Raised when ansible-pull fails or cannot be found."""


def build_ansible_pull_cmd(
    repo: str,
    dest: str,
    *,
    checkout: Optional[str] = None,
    inventory: Optional[str] = None,
    extra_args: Optional[List[str]] = None,
) -> List[str]:
    """Build a safe command list for running ansible-pull.

    Arguments:
        repo: Git repository URL or local path for ansible-pull's -U argument.
        dest: Local directory for checkout (ansible-pull -U repo -d dest).
        checkout: Optional branch/commit/tag to check out (--checkout or -C).
                  Note: ansible-pull accepts --checkout. If None, no checkout arg.
        inventory: Optional inventory file or host string to pass as -i.
        extra_args: Optional list of additional args (each element is one arg).
                    Use this to pass playbook-specific flags.

    Returns:
        List[str]: A list of command arguments suitable for subprocess.run([...]).
    """
    # Start with the executable name — resolved at runtime before executing.
    cmd: List[str] = ["ansible-pull"]

    # repository and destination are required for our wrapper's semantics
    cmd.extend(["-U", repo, "-d", dest])

    # Optional checkout/branch
    if checkout:
        # Use long form for clarity; ansible-pull supports --checkout
        cmd.extend(["--checkout", checkout])

    # Inventory may be a filename or an inventory spec; add if provided
    if inventory:
        cmd.extend(["-i", inventory])

    # Append any additional args provided by the caller
    if extra_args:
        # We trust caller to pass safe args as separate list items
        cmd.extend(list(extra_args))

    # Ensure we always run a consistent command; do not inject environment or shell
    return cmd


def run_ansible_pull(
    cmd: List[str],
    *,
    timeout: int = 300,
    capture_output: bool = True,
    check: bool = True,
    dry_run: bool = False,
) -> subprocess.CompletedProcess:
    """Execute the prepared ansible-pull command.

    Arguments:
        cmd: Command list as returned by build_ansible_pull_cmd.
        timeout: Timeout seconds for subprocess.run.
        capture_output: If True, capture stdout/stderr.
        check: If True, raise CalledProcessError on non-zero exit.
        dry_run: If True, do not execute; instead log and return a fake CompletedProcess.

    Returns:
        subprocess.CompletedProcess: The result of subprocess.run.

    Raises:
        AnsiblePullError: If ansible-pull is not found or execution fails.
    """
    # Validate that the ansible-pull executable is available on PATH
    if shutil.which("ansible-pull") is None:
        # Fail fast with a clear exception
        raise AnsiblePullError("ansible-pull not found in PATH")

    # Defensive copy to avoid callers mutating after invocation
    cmd_copy = list(cmd)

    # Log the command at debug level for maintainers/troubleshooting
    logger.debug("Running ansible-pull command: %s", cmd_copy)

    # Dry-run mode is useful for tests and CI where we only want to verify the args
    if dry_run:
        # Emulate a successful subprocess.CompletedProcess with empty output
        fake = subprocess.CompletedProcess(args=cmd_copy, returncode=0, stdout=b"", stderr=b"")
        logger.info("Dry-run enabled; not executing ansible-pull")
        return fake

    # Execute the command without shell for safety/performance
    try:
        # Use text mode? Keep bytes (universal_newlines=False) to avoid extra decoding cost;
        # many callers prefer bytes and can decode if necessary. We capture output by default.
        result = subprocess.run(
            cmd_copy,
            timeout=timeout,
            capture_output=capture_output,
            check=check,
        )
        logger.info("ansible-pull finished with return code %s", result.returncode)
        return result
    except subprocess.CalledProcessError as exc:
        # Non-zero exit with check=True
        logger.error(
            "ansible-pull failed (returncode=%s). stdout=%s stderr=%s",
            exc.returncode,
            getattr(exc, "stdout", None),
            getattr(exc, "stderr", None),
        )
        raise AnsiblePullError(f"ansible-pull failed with return code {exc.returncode}") from exc
    except subprocess.SubprocessError as exc:
        # Catch other subprocess-related exceptions (TimeoutExpired, etc.)
        logger.exception("ansible-pull execution failed due to subprocess error")
        raise AnsiblePullError("ansible-pull execution failed") from exc
