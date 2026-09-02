# Main entry point
import uvicorn
import os

def main():
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(
        "unified_manager.api.app:app",
        host=host,
        port=port,
        reload=True
    )

if __name__ == "__main__":
    main()
