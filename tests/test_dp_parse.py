from app.services.artifact_parser_service import (
    ArtifactParserService
)

report = (
    ArtifactParserService
    .parse_gitlab_dependency_report(
        "gl-dependency-scanning-report.json"
    )
)

print(report.model_dump())