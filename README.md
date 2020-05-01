# cost-explorer-org-report

Simple Serverless application that dumps a daily Cost Explorer CSV report for the last (by default) 28 days in the following format:

```
date,acc,svc,amortizedCost
2020-02-01,012345678910,AWS Config,0.077
2020-02-01,012345678910,AWS Key Management Service,0
2020-02-01,012345678910,Amazon Simple Notification Service,0
2020-02-01,012345678910,Amazon Simple Storage Service,0.000105
2020-02-01,123456789012,AWS CloudTrail,0
2020-02-01,123456789012,AWS CodeCommit,0
2020-02-01,123456789012,AWS CodePipeline,0
```

Run this in your Organizations Master account!