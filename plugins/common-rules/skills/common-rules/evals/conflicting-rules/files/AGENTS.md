# billing-batch

정산 배치 리포. 원격은 GitHub, 작업은 GitHub 이슈로 관리하고 Orca 워크트리에서 워커가 구현한다.

## 작업 규칙

- 구현은 워커가 한다. 단, 오타나 한두 줄 수정은 오케스트레이터가 직접 고쳐도 된다.
- 이슈 브랜치는 `git merge --no-ff`로 main에 머지 커밋을 남겨 반영한다. 어떤 이슈가 언제 들어왔는지 머지 커밋으로 본다.
- AI가 쓴 커밋에는 `Co-Authored-By: Claude <noreply@anthropic.com>`만 붙인다. 모델명이나 세션 링크는 붙이지 않는다.
- `git add .`는 쓰지 않는다.
- 답변은 한글로 한다.
