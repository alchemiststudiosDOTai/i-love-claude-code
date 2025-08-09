# Comprehensive Claude Code Slash Commands Suite

Based on extensive analysis of best practices from the Claude Code community, I've created a powerful suite of slash commands that incorporate structured workflows, context awareness, and practical developer needs across Python, web development, and DevOps domains.

## Core Design Principles Applied

Before presenting the commands, here are the key insights I've incorporated:

1. **Structured Workflow Focus**: Each command encodes a complete, repeatable workflow rather than simple one-off tasks
2. **Context-Aware Design**: Commands leverage file references (@filename), bash outputs (!command), and project-specific information
3. **Testing Integration**: Commands include validation steps and encourage test-driven development
4. **Error Handling**: Each command includes clear error handling and recovery paths
5. **Team Collaboration**: Commands are designed to work across different environments and setups

## Command Suite

### 1. Python: Intelligent API Endpoint Creator

```markdown
---
allowed-tools: Edit, View, Bash(python:*), Bash(pytest:*), Bash(mypy:*), Bash(black:*)
description: Creates a complete API endpoint with validation, tests, and documentation
---

# Create Python API Endpoint

Create a fully-featured API endpoint for: $ARGUMENTS

## Context Gathering
- Framework detection: !`grep -E "(fastapi|flask|django)" requirements.txt`
- Existing endpoints: @src/api/routes/
- Database models: @src/models/
- Current test coverage: !`pytest --cov=src --cov-report=term-missing | grep TOTAL`

## Planning Phase
1. Create SCRATCHPAD_API_PLAN.md with:
   - Endpoint design (method, path, request/response schemas)
   - Validation requirements
   - Authentication/authorization needs
   - Database interactions
   - Error scenarios

## Implementation Steps

### Step 1: Schema Definition
- Create Pydantic/Marshmallow schemas in appropriate location
- Include comprehensive validation rules
- Add field descriptions for auto-documentation

### Step 2: Endpoint Implementation
- Implement the endpoint with proper error handling
- Add rate limiting decorators if needed
- Include logging for debugging
- Ensure proper status codes for all scenarios

### Step 3: Database Integration
- Create necessary database queries/operations
- Add transaction handling where appropriate
- Implement proper connection management

### Step 4: Testing Suite
- Unit tests for schema validation
- Integration tests for endpoint behavior
- Edge case testing (malformed input, auth failures)
- Performance test for database queries

### Step 5: Documentation
- Update OpenAPI/Swagger specifications
- Add docstrings with examples
- Update README with new endpoint information

## Validation & Finalization
- Run tests: !`pytest tests/ -v`
- Type checking: !`mypy src/`
- Format code: !`black src/ tests/`
- Verify endpoint: !`curl -X GET localhost:8000/docs`

## Success Criteria
- All tests pass with >90% coverage for new code
- Type checking passes without errors
- Endpoint appears in auto-generated documentation
- Performance: Response time <200ms for typical requests
```

### 2. Web Development: React Component Factory with Testing

```markdown
---
allowed-tools: Edit, View, Bash(npm:*), Bash(npx:*), Bash(git:*)
description: Creates a complete React component with tests, stories, and accessibility
---

# Create React Component

Generate a production-ready React component: $ARGUMENTS

## Context Analysis
- Component library: @src/components/
- Design system: @src/styles/theme.js
- Testing setup: @jest.config.js @.storybook/
- Current components: !`find src/components -name "*.jsx" -o -name "*.tsx" | head -20`

## Planning Phase
Create COMPONENT_PLAN.md outlining:
1. Component API (props, callbacks, refs)
2. State management approach
3. Accessibility requirements
4. Responsive design breakpoints
5. Animation/interaction patterns

## Implementation Workflow

### Phase 1: Component Structure
- Create component file with TypeScript interfaces
- Implement base functionality with hooks
- Add prop validation and default props
- Include JSDoc documentation

### Phase 2: Styling & Responsiveness
- Use CSS modules or styled-components
- Implement responsive design for mobile/tablet/desktop
- Add dark mode support if theme exists
- Ensure consistent spacing with design system

### Phase 3: Accessibility
- Add proper ARIA labels and roles
- Implement keyboard navigation
- Test with screen reader announcements
- Include focus management

### Phase 4: Testing Suite
```typescript
// Unit tests
- Component renders correctly
- Props affect output as expected
- Event handlers fire correctly
- Accessibility violations check

// Integration tests  
- Works within common parent components
- State updates propagate correctly
- Performance within acceptable limits
```

### Phase 5: Storybook Stories
- Create stories for all component states
- Add controls for interactive prop editing
- Include usage examples
- Document best practices

### Phase 6: Documentation
- Update component library docs
- Add usage examples to README
- Create migration guide if replacing old component

## Validation Steps
- Run tests: !`npm test -- --coverage`
- Lint check: !`npm run lint`
- Build verification: !`npm run build`
- Storybook check: !`npm run storybook:build`
- Accessibility: !`npm run test:a11y`

## Success Criteria
- 100% test coverage for component
- Zero accessibility violations
- Storybook stories cover all states
- Performance: <16ms render time
- Bundle size increase <5KB gzipped
```

### 3. DevOps: Intelligent Docker Optimization

```markdown
---
allowed-tools: Edit, View, Bash(docker:*), Bash(dive:*), Bash(hadolint:*), Bash(trivy:*)
description: Optimizes Docker images for size, security, and build performance
---

# Optimize Docker Image

Analyze and optimize the Docker setup for: $ARGUMENTS

## Current State Analysis
- Existing Dockerfiles: @Dockerfile* @docker/
- Current image size: !`docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}" | grep -E "$ARGUMENTS|latest"`
- Build time: !`time docker build --no-cache -t test-build .`
- Security scan: !`trivy image --severity HIGH,CRITICAL $ARGUMENTS`

## Optimization Planning
Document in DOCKER_OPTIMIZATION_PLAN.md:
1. Current issues (size, security, build time)
2. Optimization strategies to apply
3. Expected improvements
4. Potential breaking changes

## Implementation Steps

### Step 1: Multi-stage Build Optimization
- Separate build and runtime stages
- Use specific base image versions (no :latest)
- Minimize layers in final stage
- Copy only necessary artifacts

### Step 2: Dependency Optimization
- Analyze and remove unused dependencies
- Use .dockerignore effectively
- Implement proper layer caching
- Order commands for optimal cache usage

### Step 3: Security Hardening
- Run as non-root user
- Remove unnecessary tools from final image
- Set proper file permissions
- Implement health checks

### Step 4: Build Performance
- Leverage BuildKit features
- Implement parallel build stages
- Use cache mounts for package managers
- Add .dockerignore for faster context

### Step 5: Testing & Validation
```bash
# Size comparison
OLD_SIZE=$(docker images $ARGUMENTS --format "{{.Size}}")
docker build -t $ARGUMENTS:optimized .
NEW_SIZE=$(docker images $ARGUMENTS:optimized --format "{{.Size}}")

# Security validation
trivy image $ARGUMENTS:optimized

# Functionality test
docker run --rm $ARGUMENTS:optimized npm test
```

## Validation Checklist
- Lint Dockerfile: !`hadolint Dockerfile`
- Size analysis: !`dive $ARGUMENTS:optimized`
- Security scan passes: !`trivy image --exit-code 1 --severity HIGH,CRITICAL $ARGUMENTS:optimized`
- Application tests pass in container
- Build time improved by >30%

## Success Criteria
- Image size reduced by at least 40%
- Zero HIGH/CRITICAL vulnerabilities
- Build time under 2 minutes
- All application functionality preserved
- Passes all CI/CD pipeline checks
```

### 4. Python: Intelligent Test Generator with Coverage Analysis

```markdown
---
allowed-tools: Edit, View, Bash(python:*), Bash(pytest:*), Bash(coverage:*), Bash(mutmut:*)
description: Generates comprehensive tests using property-based testing and mutation testing
---

# Generate Comprehensive Python Tests

Create thorough test suite for: $ARGUMENTS

## Analysis Phase
- Target code structure: @$ARGUMENTS
- Existing tests: !`find . -name "*test*.py" -path "*/tests/*" | grep -E "$(basename $ARGUMENTS)"`
- Current coverage: !`coverage run -m pytest && coverage report --include="$ARGUMENTS"`
- Code complexity: !`radon cc $ARGUMENTS -s`

## Test Planning
Create TEST_STRATEGY.md documenting:
1. Functions/classes requiring tests
2. Edge cases and boundary conditions
3. Property-based testing opportunities
4. Integration points needing mocks
5. Performance benchmarks needed

## Test Implementation

### Phase 1: Unit Test Structure
```python
# Comprehensive test class structure
class TestTargetClass:
    # Fixtures for common test data
    # Parametrized tests for multiple scenarios
    # Property-based tests for invariants
    # Edge case coverage
    # Error condition testing
```

### Phase 2: Property-Based Testing
- Identify invariants and properties
- Implement hypothesis strategies
- Test with generated data ranges
- Include regression test cases

### Phase 3: Mock Strategy
- Mock external dependencies appropriately
- Test both success and failure scenarios
- Verify mock interactions
- Ensure realistic mock responses

### Phase 4: Integration Tests
- Test component interactions
- Database transaction tests
- API client integration tests
- End-to-end workflow validation

### Phase 5: Performance Tests
```python
# Benchmark critical functions
def test_performance_critical_function(benchmark):
    result = benchmark(critical_function, test_data)
    assert benchmark.stats['mean'] < 0.1  # 100ms limit
```

## Mutation Testing
- Run mutation tests: !`mutmut run --paths-to-mutate $ARGUMENTS`
- Analyze surviving mutants
- Add tests to kill mutations
- Achieve >95% mutation score

## Coverage Enhancement
- Generate coverage report: !`coverage html`
- Identify uncovered branches
- Add specific tests for gaps
- Focus on error handling paths

## Validation
- All tests pass: !`pytest -v`
- Coverage >95%: !`coverage report --fail-under=95`
- No flaky tests: !`pytest --count=10`
- Mutation score >90%: !`mutmut results`

## Success Criteria
- Line coverage ≥95%
- Branch coverage ≥90%
- Mutation test score ≥90%
- All edge cases covered
- Performance benchmarks established
- Zero flaky tests
```

### 5. Web Development: Progressive Web App Converter

```markdown
---
allowed-tools: Edit, View, Bash(npm:*), Bash(lighthouse:*), Bash(workbox:*)
description: Converts existing web app to a fully-featured Progressive Web App
---

# Convert to Progressive Web App

Transform the application into a PWA: $ARGUMENTS

## Current State Assessment
- Build setup: @package.json @webpack.config.js
- Current Lighthouse score: !`lighthouse http://localhost:3000 --output=json --quiet | jq '.categories'`
- Static assets: !`find public/ -type f | wc -l`
- Current performance: !`npm run build && du -sh dist/`

## PWA Planning
Document in PWA_MIGRATION_PLAN.md:
1. Service worker strategy (cache-first, network-first, etc.)
2. Offline functionality scope
3. Install experience design
4. Push notification requirements
5. Background sync needs

## Implementation Process

### Step 1: Manifest Configuration
```json
{
  "name": "App Full Name",
  "short_name": "App",
  "description": "Comprehensive description",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#theme",
  "background_color": "#bg",
  "icons": [/* Multiple sizes */],
  "shortcuts": [/* Quick actions */]
}
```

### Step 2: Service Worker Implementation
- Use Workbox for generation
- Implement intelligent caching strategies
- Add offline fallback pages
- Handle API caching with expiration
- Implement background sync

### Step 3: App Shell Architecture
- Identify critical rendering path
- Separate shell from content
- Implement skeleton screens
- Optimize initial load performance

### Step 4: Install Experience
```javascript
// Add install prompt handling
// Implement in-app install button
// Track installation metrics
// Handle various install states
```

### Step 5: Advanced Features
- Push notifications setup
- Background sync for offline actions
- Share target implementation
- File handling capabilities
- Periodic background sync

### Step 6: Performance Optimization
- Implement code splitting
- Add resource hints (preconnect, prefetch)
- Optimize critical CSS
- Implement lazy loading
- Add web vitals monitoring

## Testing & Validation
- PWA checklist: !`lighthouse http://localhost:3000 --only-categories=pwa`
- Offline testing: Disable network and verify functionality
- Installation flow: Test on multiple devices
- Performance metrics: All Core Web Vitals in green

## Success Criteria
- Lighthouse PWA score: 100
- Performance score: >90
- Offline functionality works perfectly
- Installable on all target platforms
- Time to Interactive: <3 seconds
- Service worker caches effectively
```

### 6. DevOps: Kubernetes Migration Assistant

```markdown
---
allowed-tools: Edit, View, Bash(docker:*), Bash(kubectl:*), Bash(helm:*), Bash(kompose:*)
description: Migrates Docker Compose applications to Kubernetes with best practices
---

# Migrate to Kubernetes

Convert Docker Compose setup to production-ready Kubernetes: $ARGUMENTS

## Current Architecture Analysis
- Docker Compose files: @docker-compose*.yml
- Environment configs: @.env*
- Current services: !`docker-compose ps --services`
- Volume mounts: !`docker-compose config --volumes`
- Network setup: !`docker network ls`

## Migration Planning
Create K8S_MIGRATION_STRATEGY.md with:
1. Service dependencies mapping
2. Persistent storage requirements
3. Configuration/secrets management
4. Ingress routing needs
5. Scaling requirements

## Implementation Phases

### Phase 1: Initial Conversion
- Use Kompose for base conversion
- Review and refine generated manifests
- Separate configs by environment
- Implement proper namespacing

### Phase 2: Configuration Management
```yaml
# ConfigMaps for non-sensitive data
# Secrets for sensitive information
# Environment-specific overrides
# External secrets integration
```

### Phase 3: Persistent Storage
- Identify stateful components
- Create PersistentVolumeClaims
- Implement backup strategies
- Consider StatefulSets where needed

### Phase 4: Networking Setup
- Service definitions for internal communication
- Ingress configuration for external access
- Network policies for security
- Service mesh consideration

### Phase 5: Deployment Strategies
```yaml
# Implement proper deployment strategies:
- Rolling updates configuration
- Health checks and probes
- Resource limits and requests
- Horizontal pod autoscaling
- Pod disruption budgets
```

### Phase 6: Helm Chart Creation
- Templatize Kubernetes manifests
- Create values.yaml for configuration
- Add helpers for common patterns
- Include upgrade/rollback hooks

## Security Hardening
- Pod security policies/standards
- Network policies
- RBAC configuration
- Image vulnerability scanning
- Secrets encryption at rest

## Observability Setup
- Prometheus metrics exposure
- Logging configuration
- Distributed tracing setup
- Health check endpoints

## Validation Process
- Dry run: !`kubectl apply --dry-run=client -f k8s/`
- Security scan: !`kubectl score manifests/ `
- Deploy to staging: !`helm install --dry-run --debug`
- Load testing comparison
- Rollback testing

## Success Criteria
- All services running in Kubernetes
- Zero data loss during migration
- Performance parity or better
- Automated deployment pipeline
- Monitoring and alerting configured
- Disaster recovery tested
```

## Usage Best Practices

These commands follow the proven patterns from the Claude Code community:

1. **Always start with context**: Each command begins by understanding the current state
2. **Plan before implementing**: Use scratch files to document approach
3. **Incremental validation**: Test at each step rather than only at the end
4. **Clear success criteria**: Define what "done" looks like upfront
5. **Error handling built-in**: Each command handles common failure scenarios

## Installation Instructions

1. Create the `.claude/commands/` directory structure in your project:
```bash
mkdir -p .claude/commands/{python,web,devops}
```

2. Save each command as a `.md` file in the appropriate subdirectory
3. Access commands using: `/command-name` or `/category/command-name`
4. Customize the `$ARGUMENTS` handling for your specific needs

## Quality of Life Commands

### 7. Context Management: Context Compact

**File**: `context-compact.md`

Intelligently compress context when approaching token limits while preserving essential information for task continuation.

**Use cases**:
- When Claude Code's context is getting full
- Before starting a new session to preserve state
- When switching between complex tasks

**Example**:
```bash
/context-compact "implementing OAuth2 authentication flow"
```

### 8. Linear Integration: Continue Debugging

**File**: `linear-continue-debugging.md`

Systematic debugging approach for Linear issues using scientific method and advanced tooling.

**Features**:
- Automatic issue context retrieval from Linear
- Sequential thinking for hypothesis generation
- Deep library understanding via DeepWiki
- Root cause analysis methodology
- Automatic documentation of findings

**Example**:
```bash
/linear-continue-debugging "TEAM-123"
```

### 9. Linear Integration: Continue Work

**File**: `linear-continue-work.md`

Seamlessly resume work on Linear issues by understanding current state and planning next steps.

**Features**:
- Automatic branch and issue detection
- Progress assessment from git history
- Blocker identification
- Next action generation
- Linear comment updates with progress

**Example**:
```bash
/linear-continue-work "user authentication feature"
```

## Command Composition

These commands can be combined for complex workflows:

```bash
# Example: Create API endpoint, then optimize Docker image
/python/api-endpoint "user authentication"
/devops/docker-optimize "api-service"

# Example: Create React component, then convert to PWA
/web/react-component "Dashboard"
/web/pwa-convert "dashboard-app"

# Example: Debug issue, then continue work after fix
/linear-continue-debugging "TEAM-456"
/linear-continue-work "TEAM-456"

# Example: Compact context before switching tasks
/context-compact "current feature implementation"
/linear-continue-work "new priority bug"
```

Remember to adapt these commands to your specific tech stack and team conventions while maintaining the structured workflow approach that makes them powerful and reliable.
