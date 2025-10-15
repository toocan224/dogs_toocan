using System;

namespace DogTrainingWeb.Models
{
    public class TrainingSchedule
    {
        public long Id { get; set; }
        public string DogName { get; set; }
        public DateTime StartTime { get; set; }
        public DateTime EndTime { get; set; }
        public string TrainingType { get; set; }
        public bool IsCompleted { get; set; }
    }
}