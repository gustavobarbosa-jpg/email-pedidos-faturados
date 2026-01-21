
import sys
import argparse
from typing import List, Optional

from src.orchestration.pipeline import PipelineOrchestrator
from src.utils.logger import pipeline_logger
from src.config.settings import BUSINESS_RULES


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Email Reports Pipeline - Send personalized reports to managers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Process all managers
  python main.py --teams 200 300          # Process specific teams
  python main.py --validate                 # Validation mode only
  python main.py --teams 200 --validate    # Validate specific teams
        """
    )
    
    parser.add_argument(
        '--teams', 
        nargs='+', 
        type=int, 
        help='Team codes to process (space-separated)'
    )
    
    parser.add_argument(
        '--validate', 
        action='store_true',
        help='Run in validation mode (no email sending)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def main():
    """Main execution function."""
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Set logging level
        if args.verbose:
            import logging
            logging.getLogger().setLevel(logging.DEBUG)
        
        # Initialize pipeline
        orchestrator = PipelineOrchestrator()
        
        # Display pipeline information
        pipeline_logger.info("Starting Email Reports Pipeline")
        pipeline_logger.info(f"Pipeline ID: {orchestrator.pipeline_id}")
        pipeline_logger.info(f"Business Rules: {BUSINESS_RULES.valid_companies}")
        
        if args.teams:
            pipeline_logger.info(f"Processing teams: {args.teams}")
        else:
            pipeline_logger.info("Processing all teams")
        
        if args.validate:
            pipeline_logger.info("Running in VALIDATION mode")
        else:
            pipeline_logger.info("Running in PRODUCTION mode")
        
        # Run pipeline
        if args.validate:
            results = orchestrator.run_validation_mode(args.teams)
        else:
            results = orchestrator.run_pipeline(args.teams)
        
        # Display results
        display_results(results)
        
        # Exit with appropriate code
        sys.exit(0 if results['success'] else 1)
        
    except KeyboardInterrupt:
        pipeline_logger.info("Pipeline interrupted by user")
        sys.exit(130)
    except Exception as e:
        pipeline_logger.error(f"Pipeline failed with unhandled error", e)
        sys.exit(1)


def display_results(results: dict):
    """Display pipeline execution results."""
    print("\n" + "="*60)
    print("PIPELINE EXECUTION RESULTS")
    print("="*60)
    
    if results.get('early_exit'):
        # Handle early exit case
        print(f"⚠️  Pipeline stopped early!")
        print(f"📊 Pipeline ID: {results['pipeline_id']}")
        print(f"⏱️  Duration: {results['duration']:.2f} seconds")
        print(f"🚫 Reason: {results['early_exit_reason']}")
        
        if results['early_exit_reason'] == "Semantic model validation failed":
            print("\n📧 Alert email sent to: gustavo.barbosa@vilanova.com.br")
            print("❌ No reports were sent to managers")
            print("🔄 Please check semantic model update and try again")
        
    elif results['success']:
        print(f"✅ Pipeline completed successfully!")
        print(f"📊 Pipeline ID: {results['pipeline_id']}")
        print(f"⏱️  Duration: {results['duration']:.2f} seconds")
        
        if 'results' in results:
            res = results['results']
            stats = res['statistics']
            
            print(f"\n📈 SUMMARY:")
            print(f"   Managers processed: {res['total_managers']}")
            print(f"   Successful: {res['successful']}")
            print(f"   Failed: {res['failed']}")
            print(f"   Success rate: {res['successful']/res['total_managers']*100:.1f}%")
            
            print(f"\n📊 DATA STATISTICS:")
            print(f"   Total records: {stats['total_records']:,}")
            print(f"   Faturados: {stats['total_faturados']:,}")
            print(f"   Pendentes: {stats['total_pendentes']:,}")
            print(f"   Total Ingressado: {stats['total_ingressado']:,.2f}")
            
            if res['errors']:
                print(f"\n⚠️  ERRORS ({len(res['errors'])}):")
                for i, error in enumerate(res['errors'][:3], 1):
                    manager = error['manager']
                    print(f"   {i}. Team {manager.get('equipe')}: {error['error']}")
                
                if len(res['errors']) > 3:
                    print(f"   ... and {len(res['errors']) - 3} more errors")
    else:
        print(f"❌ Pipeline failed!")
        print(f"📊 Pipeline ID: {results['pipeline_id']}")
        print(f"⏱️  Duration: {results.get('duration', 0):.2f} seconds")
        print(f"🚫 Error: {results.get('error', 'Unknown error')}")
    
    print("="*60)


if __name__ == "__main__":
    main()
